class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.environment = {}
        self.tables = {}

    def evaluate(self, node):
        if node.type == 'Literal':
            return node._env
        elif node.type == 'Identifier':
            return self.environment[node._env]
        elif node.type == 'Expression':
            try:
                value = eval(node._env, self.environment)
                return value
            except Exception as e:
                raise RuntimeError(f"Error evaluating expression {node._env}: {e}")
        elif node.type == 'Table':
            if node._env not in self.tables:
                self.tables[node._env] = {}
            if node.children:
                for child in node.children:
                    if child.type == 'Pass':
                        continue
                    self.evaluate(child)
            return self.tables[node._env]
        elif node.type == 'Assignment':
            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])
            if isinstance(left, dict):
                key = node.children[0]._env
                self.tables[key][right] = right
            else:
                self.environment[left] = right
        elif node.type == 'ImportStatement':
            module_name = node._env
            module = __import__(module_name)
            self.environment[module_name] = module
        elif node.type == 'FromImportStatement':
            module_name, name, alias = node._env
            module = __import__(module_name)
            if alias:
                self.environment[alias] = getattr(module, name)
            else:
                self.environment[name] = getattr(module, name)
        elif node.type == 'ExpressionStatement':
            return self.evaluate(node.children[0])
        elif node.type == 'Block':
            for statement in node.children:
                self.evaluate(statement)
        elif node.type == 'Pass':
            pass
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    def run(self):
        self.evaluate(self.ast)


    def get_result(self):
        return self.tables, self.environment

# Generated from antlr4_grammar/hyconfiglanguage.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .hyconfiglanguageParser import hyconfiglanguageParser
else:
    from hyconfiglanguageParser import hyconfiglanguageParser

# This class defines a complete listener for a parse tree produced by hyconfiglanguageParser.
class hyconfiglanguageListener(ParseTreeListener):

    # Enter a parse tree produced by hyconfiglanguageParser#configFile.
    def enterConfigFile(self, ctx:hyconfiglanguageParser.ConfigFileContext):
        pass

    # Exit a parse tree produced by hyconfiglanguageParser#configFile.
    def exitConfigFile(self, ctx:hyconfiglanguageParser.ConfigFileContext):
        pass


    # Enter a parse tree produced by hyconfiglanguageParser#definition.
    def enterDefinition(self, ctx:hyconfiglanguageParser.DefinitionContext):
        pass

    # Exit a parse tree produced by hyconfiglanguageParser#definition.
    def exitDefinition(self, ctx:hyconfiglanguageParser.DefinitionContext):
        pass


    # Enter a parse tree produced by hyconfiglanguageParser#tableDef.
    def enterTableDef(self, ctx:hyconfiglanguageParser.TableDefContext):
        pass

    # Exit a parse tree produced by hyconfiglanguageParser#tableDef.
    def exitTableDef(self, ctx:hyconfiglanguageParser.TableDefContext):
        pass


    # Enter a parse tree produced by hyconfiglanguageParser#varDef.
    def enterVarDef(self, ctx:hyconfiglanguageParser.VarDefContext):
        pass

    # Exit a parse tree produced by hyconfiglanguageParser#varDef.
    def exitVarDef(self, ctx:hyconfiglanguageParser.VarDefContext):
        pass


    # Enter a parse tree produced by hyconfiglanguageParser#importStmt.
    def enterImportStmt(self, ctx:hyconfiglanguageParser.ImportStmtContext):
        pass

    # Exit a parse tree produced by hyconfiglanguageParser#importStmt.
    def exitImportStmt(self, ctx:hyconfiglanguageParser.ImportStmtContext):
        pass



del hyconfiglanguageParser
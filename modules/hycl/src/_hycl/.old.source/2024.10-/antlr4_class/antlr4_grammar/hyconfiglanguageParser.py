# Generated from antlr4_grammar/hyconfiglanguage.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,8,39,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,5,0,12,8,0,
        10,0,12,0,15,9,0,1,0,1,0,1,1,1,1,1,1,3,1,22,8,1,1,2,1,2,1,2,1,2,
        1,3,1,3,1,3,1,3,1,4,1,4,3,4,34,8,4,1,4,1,4,1,4,1,4,0,0,5,0,2,4,6,
        8,0,0,37,0,13,1,0,0,0,2,21,1,0,0,0,4,23,1,0,0,0,6,27,1,0,0,0,8,33,
        1,0,0,0,10,12,3,2,1,0,11,10,1,0,0,0,12,15,1,0,0,0,13,11,1,0,0,0,
        13,14,1,0,0,0,14,16,1,0,0,0,15,13,1,0,0,0,16,17,5,0,0,1,17,1,1,0,
        0,0,18,22,3,4,2,0,19,22,3,6,3,0,20,22,3,8,4,0,21,18,1,0,0,0,21,19,
        1,0,0,0,21,20,1,0,0,0,22,3,1,0,0,0,23,24,5,1,0,0,24,25,5,6,0,0,25,
        26,5,2,0,0,26,5,1,0,0,0,27,28,5,6,0,0,28,29,5,3,0,0,29,30,5,7,0,
        0,30,7,1,0,0,0,31,32,5,4,0,0,32,34,5,6,0,0,33,31,1,0,0,0,33,34,1,
        0,0,0,34,35,1,0,0,0,35,36,5,5,0,0,36,37,5,6,0,0,37,9,1,0,0,0,3,13,
        21,33
    ]

class hyconfiglanguageParser ( Parser ):

    grammarFileName = "hyconfiglanguage.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'['", "']'", "'='", "'from'", "'import'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "NAME", "VALUE", "INDENT" ]

    RULE_configFile = 0
    RULE_definition = 1
    RULE_tableDef = 2
    RULE_varDef = 3
    RULE_importStmt = 4

    ruleNames =  [ "configFile", "definition", "tableDef", "varDef", "importStmt" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    NAME=6
    VALUE=7
    INDENT=8

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ConfigFileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(hyconfiglanguageParser.EOF, 0)

        def definition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(hyconfiglanguageParser.DefinitionContext)
            else:
                return self.getTypedRuleContext(hyconfiglanguageParser.DefinitionContext,i)


        def getRuleIndex(self):
            return hyconfiglanguageParser.RULE_configFile

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConfigFile" ):
                listener.enterConfigFile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConfigFile" ):
                listener.exitConfigFile(self)




    def configFile(self):

        localctx = hyconfiglanguageParser.ConfigFileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_configFile)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 114) != 0):
                self.state = 10
                self.definition()
                self.state = 15
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 16
            self.match(hyconfiglanguageParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefinitionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def tableDef(self):
            return self.getTypedRuleContext(hyconfiglanguageParser.TableDefContext,0)


        def varDef(self):
            return self.getTypedRuleContext(hyconfiglanguageParser.VarDefContext,0)


        def importStmt(self):
            return self.getTypedRuleContext(hyconfiglanguageParser.ImportStmtContext,0)


        def getRuleIndex(self):
            return hyconfiglanguageParser.RULE_definition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefinition" ):
                listener.enterDefinition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefinition" ):
                listener.exitDefinition(self)




    def definition(self):

        localctx = hyconfiglanguageParser.DefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_definition)
        try:
            self.state = 21
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 18
                self.tableDef()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 19
                self.varDef()
                pass
            elif token in [4, 5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 20
                self.importStmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TableDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(hyconfiglanguageParser.NAME, 0)

        def getRuleIndex(self):
            return hyconfiglanguageParser.RULE_tableDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTableDef" ):
                listener.enterTableDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTableDef" ):
                listener.exitTableDef(self)




    def tableDef(self):

        localctx = hyconfiglanguageParser.TableDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_tableDef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self.match(hyconfiglanguageParser.T__0)
            self.state = 24
            self.match(hyconfiglanguageParser.NAME)
            self.state = 25
            self.match(hyconfiglanguageParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(hyconfiglanguageParser.NAME, 0)

        def VALUE(self):
            return self.getToken(hyconfiglanguageParser.VALUE, 0)

        def getRuleIndex(self):
            return hyconfiglanguageParser.RULE_varDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarDef" ):
                listener.enterVarDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarDef" ):
                listener.exitVarDef(self)




    def varDef(self):

        localctx = hyconfiglanguageParser.VarDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_varDef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.match(hyconfiglanguageParser.NAME)
            self.state = 28
            self.match(hyconfiglanguageParser.T__2)
            self.state = 29
            self.match(hyconfiglanguageParser.VALUE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImportStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(hyconfiglanguageParser.NAME)
            else:
                return self.getToken(hyconfiglanguageParser.NAME, i)

        def getRuleIndex(self):
            return hyconfiglanguageParser.RULE_importStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImportStmt" ):
                listener.enterImportStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImportStmt" ):
                listener.exitImportStmt(self)




    def importStmt(self):

        localctx = hyconfiglanguageParser.ImportStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_importStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 31
                self.match(hyconfiglanguageParser.T__3)
                self.state = 32
                self.match(hyconfiglanguageParser.NAME)


            self.state = 35
            self.match(hyconfiglanguageParser.T__4)
            self.state = 36
            self.match(hyconfiglanguageParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx






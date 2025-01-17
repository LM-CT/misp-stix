import stix2patterns.v20.object_validator as validator_v20
import stix2patterns.v21.object_validator as validator_v21
from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from stix2patterns.exceptions import STIXPatternErrorListener
from stix2patterns.v20.grammars.STIXPatternLexer import STIXPatternLexer as lexer_v20
from stix2patterns.v20.grammars.STIXPatternParser import STIXPatternParser as parser_v20
from stix2patterns.v20.inspector import InspectionListener as inspector_v20
from stix2patterns.v21.grammars.STIXPatternLexer import STIXPatternLexer as lexer_v21
from stix2patterns.v21.grammars.STIXPatternParser import STIXPatternParser as parser_v21
from stix2patterns.v21.inspector import InspectionListener as inspector_v21

_VALID_VERSIONS = ('2.0', '2.1')


class STIX2PatternParser:
    def __init__(self, version: str):
        self.__version = version.strip('.') if version in _VALID_VERSIONS else '2.1'

    @property
    def pattern(self):
        return self.__pattern_data

    @property
    def valid(self) -> bool:
        return self.__valid

    @property
    def version(self) -> str:
        return self.__version

    def load_stix_pattern(self, pattern_str: str):
        getattr(self, f'_load_stix_{self.version}_pattern')(pattern_str)

    def _load_stix_20_pattern(self, pattern_str: str):
        pattern = InputStream(pattern_str)
        parseErrListener = STIXPatternErrorListener()
        lexer = lexer_v20(pattern)
        lexer.removeErrorListeners()
        stream = CommonTokenStream(lexer)
        parser = parser_v20(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(parseErrListener)
        for i, lit_name in enumerate(parser.literalNames):
            if lit_name == u"<INVALID>":
                parser.literalNames[i] = parser.symbolicNames[i]
        tree = parser.pattern()
        inspection_listener = inspector_v20()
        if len(parseErrListener.err_strings) == 0:
            ParseTreeWalker.DEFAULT.walk(inspection_listener, tree)
            pattern_data = inspection_listener.pattern_data()
            obj_validator_results = validator_v20.verify_object(pattern_data)
            if obj_validator_results:
                parseErrListener.err_strings.extend(obj_validator_results)
            else:
                self.__pattern_data = pattern_data
        self.__valid = (len(parseErrListener.err_strings) == 0)

    def _load_stix_21_pattern(self, pattern_str: str):
        pattern = InputStream(pattern_str)
        parseErrListener = STIXPatternErrorListener()
        lexer = lexer_v21(pattern)
        lexer.removeErrorListeners()
        stream = CommonTokenStream(lexer)
        parser = parser_v21(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(parseErrListener)
        for i, lit_name in enumerate(parser.literalNames):
            if lit_name == u"<INVALID>":
                parser.literalNames[i] = parser.symbolicNames[i]
        tree = parser.pattern()
        inspection_listener = inspector_v21()
        if len(parseErrListener.err_strings) == 0:
            ParseTreeWalker.DEFAULT.walk(inspection_listener, tree)
            pattern_data = inspection_listener.pattern_data()
            obj_validator_results = validator_v21.verify_object(pattern_data)
            if obj_validator_results:
                parseErrListener.err_strings.extend(obj_validator_results)
            else:
                self.__pattern_data = pattern_data
        self.__valid = (len(parseErrListener.err_strings) == 0)
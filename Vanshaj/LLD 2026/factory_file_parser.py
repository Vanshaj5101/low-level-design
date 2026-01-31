"""
Problem Context:
This exercise is designed to practice and reinforce understanding of the
Factory Method design pattern using a File parse system.

An application needs to support parsing multiple file formats (e.g. JSON,
CSV, XML). Each file format requires a different parsing implementation, but
the client code should remain unaware of the concrete parse classes used.

Design Goals:
- Decouple file parsing logic from object creation
- Allow the system to select the appropriate parse at runtime
- Make the system easy to extend when new file formats are added
- Avoid conditional logic (if/else) in client code for parse creation

Functional Requirements:
- Define a common Fileparse interface with a parse(file_path) method
- Implement concrete parses for:
    - JSON files
    - CSV files
    - XML files
- Implement a FileparseFactory that returns the correct parse based on
  the file type provided
- Client code must use the factory to obtain parses and must not directly
  instantiate concrete parse classes

Why This Matters:
This is a common real-world use case where Factory Method is applied to handle
multiple implementations of a common interface while keeping the client code
clean, maintainable, and open for extension but closed for modification.

This exercise helps validate understanding of:
- Factory Method pattern
- Programming to an interface
- Separation of concerns
- Extensibility in object-oriented design
"""


from abc import ABC, abstractmethod


class FileParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> str:
        pass


class JSONParser(FileParser):
    def parse(self, content: str) -> str:
        return f"JSON parsed: {content}"


class CSVParser(FileParser):
    def parse(self, content: str) -> str:
        return f"CSV parsed: {content}"


class XMLParser(FileParser):
    def parse(self, content: str) -> str:
        return f"XML parsed: {content}"


class FileParserFactory:
    _registry = {"json": JSONParser, "csv": CSVParser, "xml": XMLParser}

    @classmethod
    def get_file_parser(cls, kind: str) -> FileParser:
        kind = kind.lower()
        parser_cls = cls._registry.get(kind)
        if not parser_cls:
            raise ValueError(f"Unsupported file type: {kind}")
        return parser_cls()


print(FileParserFactory.get_file_parser("json").parse("Hello world!!!"))
print(FileParserFactory.get_file_parser("csv").parse("Hello world!!!"))
print(FileParserFactory.get_file_parser("xml").parse("Hello world!!!"))

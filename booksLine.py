import re
from collections import defaultdict
from abc import ABC, abstractmethod
from typing import Callable, Iterable, List, Dict, Set, Any


"""
Strategy

MatchStrategy lets us plug in SimpleKeywordMatcher, FuzzyMatcher, or any future algorithm.

Facade

IndexService and NameFinder hide the choice of matching behind simple build_index()/find() APIs.

Factory Method (implicit)

NameFinder's constructor picks and configures the right matcher without client code calling the matcher class directly.
"""


class CharacterRegistry:
    """Maintain the set of character names to index."""

    def __init__(self):
        self._names: Set[str] = set()

    def add(self, name: str) -> None:
        """Register a new character (e.g. "Harry")."""
        self._names.add(name)

    def remove(self, name: str) -> None:
        """Remove a character from indexing."""
        self._names.discard(name)

    def get_all(self) -> List[str]:
        """Return a list of all registered names."""
        return list(self._names)


# --- Strategy Interface ---
class MatchStrategy(ABC):
    @abstractmethod
    def compile(self, names: List[str]) -> None: ...
    @abstractmethod
    def match(self, line: str) -> List[str]: ...


# --- Exact Keyword Matcher ---
class SimpleKeywordMatcher(MatchStrategy):
    def __init__(self):
        self._pattern = None
        self._name_map: Dict[str, str] = {}

    def compile(self, names: List[str]) -> None:
        escaped = [re.escape(n) for n in names]
        pat = r"\b(" + "|".join(escaped) + r")\b"
        self._pattern = re.compile(pat, re.IGNORECASE)
        self._name_map = {n.lower(): n for n in names}

    def match(self, line: str) -> List[str]:
        if self._pattern is None:
            raise RuntimeError("Must compile() first")
        found = self._pattern.findall(line)
        return [self._name_map[f.lower()] for f in found]


# --- Fuzzy Matcher ---
class FuzzyMatcher(MatchStrategy):
    def __init__(self, threshold: float = 0.8, max_matches: int = 3):
        self.threshold = threshold
        self.max_matches = max_matches
        self._names: List[str] = []

    def compile(self, names: List[str]) -> None:
        # We'll match against lowercase set for simplicity
        self._names = names

    def match(self, line: str) -> List[str]:
        results = []
        words = re.findall(r"\w+", line)
        for w in words:
            # find_close in registry
            matches = get_close_matches(
                w, self._names, n=self.max_matches, cutoff=self.threshold
            )
            results.extend(matches)
        return results


# --- NameFinder delegates to a strategy ---
class NameFinder:
    def __init__(self, strategy: MatchStrategy):
        self.strategy = strategy

    def compile(self, names: List[str]) -> None:
        self.strategy.compile(names)

    def find(self, line: str) -> List[str]:
        return self.strategy.match(line)


class IndexService:
    """
    Uses CharacterRegistry and NameFinder to build a global count
    of how often each character is mentioned across many books.
    """

    def __init__(self, registry: CharacterRegistry, finder: NameFinder):
        self.registry = registry
        self.finder = finder
        self.index: Dict[str, int] = defaultdict(int)

    def build_index(
        self, books: List[Any], get_lines: Callable[[Any], Iterable[str]]
    ) -> None:
        """
        Parse each book line by line, find all character mentions,
        and update internal counters.
        """
        # Prepare the pattern once for all books
        names = self.registry.get_all()
        self.finder.compile(names)

        # Iterate every line in every book
        for book in books:
            for line in get_lines(book):
                found = self.finder.find(line)
                for name in found:
                    self.index[name] += 1

    def get_count(self, name: str) -> int:
        """Return how many times `name` was found (0 if never)."""
        return self.index.get(name, 0)

    def get_index(self) -> Dict[str, int]:
        """Return the full character→count map."""
        return dict(self.index)


# --- Example Usage ---


def mock_get_lines(book_id: str):
    # Stub for the book‐parsing API: yields lines of text
    sample = {
        "hp1": [
            "Harry and Hermione walked through the hall.",
            "Ron hated spiders, but Harry was unafraid.",
        ],
        "lotr1": [
            "Gandalf met Bilbo Baggins in the Shire.",
            "Gollum whispered his riddles.",
        ],
    }
    for line in sample.get(book_id, []):
        yield line


if __name__ == "__main__":
    # 1. Set up registry
    registry = CharacterRegistry()
    for name in ["Harry", "Hermione", "Ron", "Gandalf", "Bilbo", "Gollum"]:
        registry.add(name)

    # 2. Build the index
    finder = NameFinder()
    indexer = IndexService(registry, finder)
    books = ["hp1", "lotr1"]
    indexer.build_index(books, mock_get_lines)

    # 3. Inspect results
    print(indexer.get_index())
    # e.g. {'Harry':2, 'Hermione':1, 'Ron':1, 'Gandalf':1, 'Bilbo':1, 'Gollum':1}

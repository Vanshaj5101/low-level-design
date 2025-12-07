import threading
import time
import uuid
from enum import Enum
from typing import Dict, List, Optional


"""
Singleton
StackOverflowSystem serves as the sole orchestrator of users, posts, votes, and services—ensuring a single point of access to core state.

Factory Method
Methods like post_question(), post_answer(), and post_comment() encapsulate object creation (Questions, Answers, Comments) so callers 
don't need to know the concrete classes or how IDs are generated.

"""


class VoteType(Enum):
    UP = 1
    DOWN = -1


class Post:
    def __init__(self, post_id: str, author_id: str, body: str):
        self.post_id = post_id
        self.author_id = author_id
        self.body = body
        self.created_at = time.time()
        self.votes = 0
        self.lock = threading.Lock()
        self.comments: List["Comment"] = []

    def add_comment(self, comment: "Comment"):
        with self.lock:
            self.comments.append(comment)

    def apply_vote(self, vt: VoteType) -> int:
        with self.lock:
            self.votes += vt.value
            return self.votes


class Question(Post):
    def __init__(
        self, post_id: str, author_id: str, title: str, body: str, tags: List[str]
    ):
        super().__init__(post_id, author_id, body)
        self.title = title
        self.tags = tags
        self.answers: List["Answer"] = []

    def add_answer(self, answer: "Answer"):
        with self.lock:
            self.answers.append(answer)


class Answer(Post):
    def __init__(self, post_id: str, author_id: str, body: str, question_id: str):
        super().__init__(post_id, author_id, body)
        self.question_id = question_id


class Comment:
    def __init__(self, comment_id: str, author_id: str, body: str, parent_id: str):
        self.comment_id = comment_id
        self.author_id = author_id
        self.body = body
        self.parent_id = parent_id
        self.created_at = time.time()


class User:
    def __init__(self, user_id: str, username: str):
        self.user_id = user_id
        self.username = username
        self.reputation = 0
        self.lock = threading.Lock()

    def change_reputation(self, delta: int):
        with self.lock:
            self.reputation += delta
            return self.reputation


class ReputationService:
    # Simple rule set; could be externalized
    POINTS = {
        ("question", VoteType.UP): 5,
        ("question", VoteType.DOWN): -2,
        ("answer", VoteType.UP): 10,
        ("answer", VoteType.DOWN): -2,
    }

    def update(self, post: Post, vt: VoteType, users: Dict[str, User]):
        kind = "question" if isinstance(post, Question) else "answer"
        delta = self.POINTS.get((kind, vt), 0)
        users[post.author_id].change_reputation(delta)


class VoteService:
    def __init__(self, rep_svc: ReputationService, users: Dict[str, User]):
        self.rep_svc = rep_svc
        self.users = users

    def vote(self, voter_id: str, post: Post, vt: VoteType):
        # In a real system, prevent double-voting, self-voting, etc.
        new_count = post.apply_vote(vt)
        self.rep_svc.update(post, vt, self.users)
        return new_count


class SearchService:
    def __init__(self, posts: Dict[str, Post]):
        self.posts = posts
        self.lock = threading.Lock()

    def search(
        self,
        keyword: Optional[str] = None,
        tags: Optional[List[str]] = None,
        author_id: Optional[str] = None,
    ) -> List[Post]:
        with self.lock:
            results = []
            for p in self.posts.values():
                if isinstance(p, Question):
                    if keyword and keyword.lower() not in (p.title + p.body).lower():
                        continue
                    if tags and not set(tags).issubset(set(p.tags)):
                        continue
                if author_id and p.author_id != author_id:
                    continue
                results.append(p)
            return results


class StackOverflowSystem:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.posts: Dict[str, Post] = {}
        self.rep_svc = ReputationService()
        self.vote_svc = VoteService(self.rep_svc, self.users)
        self.search_svc = SearchService(self.posts)
        self.lock = threading.Lock()

    def create_user(self, username: str) -> str:
        user_id = str(uuid.uuid4())
        self.users[user_id] = User(user_id, username)
        return user_id

    def post_question(
        self, user_id: str, title: str, body: str, tags: List[str]
    ) -> str:
        post_id = str(uuid.uuid4())
        q = Question(post_id, user_id, title, body, tags)
        with self.lock:
            self.posts[post_id] = q
        return post_id

    def post_answer(self, user_id: str, question_id: str, body: str) -> Optional[str]:
        if question_id not in self.posts or not isinstance(
            self.posts[question_id], Question
        ):
            return None
        post_id = str(uuid.uuid4())
        ans = Answer(post_id, user_id, body, question_id)
        with self.lock:
            self.posts[post_id] = ans
        self.posts[question_id].add_answer(ans)
        return post_id

    def post_comment(self, user_id: str, post_id: str, body: str) -> Optional[str]:
        if post_id not in self.posts:
            return None
        com_id = str(uuid.uuid4())
        com = Comment(com_id, user_id, body, post_id)
        self.posts[post_id].add_comment(com)
        return com_id

    def vote_post(self, voter_id: str, post_id: str, is_upvote: bool) -> Optional[int]:
        if post_id not in self.posts or voter_id not in self.users:
            return None
        vt = VoteType.UP if is_upvote else VoteType.DOWN
        return self.vote_svc.vote(voter_id, self.posts[post_id], vt)

    def search(
        self,
        keyword: Optional[str] = None,
        tags: Optional[List[str]] = None,
        author_id: Optional[str] = None,
    ) -> List[Post]:
        return self.search_svc.search(keyword, tags, author_id)


# --- Example Usage ---
if __name__ == "__main__":
    so = StackOverflowSystem()
    alice = so.create_user("alice")
    bob = so.create_user("bob")

    q1 = so.post_question(
        alice,
        "How to reverse a list in Python?",
        "I want to reverse a list in place without extra memory.",
        tags=["python", "list", "algorithm"],
    )

    a1 = so.post_answer(bob, q1, "You can use list.reverse() or slicing: lst[::-1].")
    so.vote_post(bob, q1, is_upvote=True)  # +5 rep to Alice
    so.vote_post(alice, a1, is_upvote=True)  # +10 rep to Bob

    results = so.search(keyword="reverse", tags=["python"])
    print(f"Search returned {len(results)} question(s).")

from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import make_review, Review, Book


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(book:Book, review_text: str, user_name: str,rating:int, repo: AbstractRepository):
    # Check that the article exists.
    if book is None:
        raise NonExistentBookException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException


    # Create review.
    review = make_review(review_text, user, book,rating)

    # Update the repository.
    repo.add_review(review)


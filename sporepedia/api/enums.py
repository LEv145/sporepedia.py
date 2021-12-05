from enum import Enum


class SearchFilter(str, Enum):
    newest = "NEWEST"
    most_popular = "MOST_POPULAR"
    most_popular_new = "MOST_POPULAR_NEW"
    featured = "FEATURED"

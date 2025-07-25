from ai.model.base_model import Base


class BlogContent(Base):
    id: str
    title: str
    url: str
    content: str

    def to_dict(self) -> dict:
        """Convert the object to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "content": self.content,
        }


class BlogTopic(Base):
    id: str
    title: str
    url: str
    blogs: list[BlogContent] = []

    def to_dict(self) -> dict:
        """Convert the object to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "blogs": [blog.to_dict() for blog in self.blogs],
        }

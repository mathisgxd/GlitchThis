from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy.ext.hybrid import hybrid_property 
from sqlalchemy import create_engine, select, delete
from typing import List
from enum import IntEnum, StrEnum

class Base(DeclarativeBase):
    pass

class ManageSession:
    _session: Session = None

    def get_session(self) -> Session:
        if self._session is None:
            self._session = Session.object_session(self)

        return self._session
    
    def commit_session(self):
        self.get_session().commit()

    def add_to_session(self, instance, commit: bool = True):
        session = self.get_session()
        session.add(instance)

        if commit:
            session.commit()

    def delete_from_session(self, instance, commit: bool = True):
        session = self.get_session()
        session.delete(instance)

        if commit:
            session.commit()

class Levels(IntEnum):
    BASIC = 0
    OWNER = 1

class User(Base, ManageSession):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int]
    level: Mapped[int]

    def set_level(self, level: int | Levels, commit: bool = True):
        self.level = level

        if commit:
            self.commit_session()

class Chat(Base, ManageSession):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int]
    level: Mapped[int]

    def set_level(self, level: int | Levels, commit: bool = True):
        self.level = level

        if commit:
            self.commit_session()

class Command(Base, ManageSession):
    __tablename__ = "commands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    level: Mapped[int]
    show: Mapped[bool]

class Medium(Base, ManageSession):
    class Types(StrEnum):
        PHOTO = "photo"
        AUDIO = "audio"

    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[str]
    file_name: Mapped[str]
    name: Mapped[str] = mapped_column(nullable=True)

    def set_name(self, name: str | None, commit: bool = True):
        self.name = name

        if commit:
            self.commit_session()

class DataSession(Session):
    @hybrid_property
    def users(self) -> List[User]:
        return self.query(User).all()
    
    @hybrid_property
    def chats(self) -> List[Chat]:
        return self.query(Chat).all()

    @hybrid_property
    def commands(self) -> List[Command]:
        return self.query(Command).all()

    @hybrid_property
    def media(self) -> List[Medium]:
        return self.query(Medium).all()

    def get(self, model, by, value):
        '''Base get method'''
        return self.scalars(select(model).where(by == value)).first()

    def get_user(self, tg_id: int) -> User:
        '''Get a user by its tg id. Returns None if not registered.'''
        return self.get(User, User.tg_id, tg_id)

    def get_chat(self, tg_id: int) -> Chat:
        '''Get a chat by its tg id. Returns None if not registered.'''
        return self.get(Chat, Chat.tg_id, tg_id)

    def get_command(self, name: str) -> Command:
        '''Get a command by its name. Returns None if not registered.'''
        return self.get(Command, Command.name, name)

    def get_medium(self, name: str) -> Medium:
        '''Get a medium by its name. Returns None if not registered.'''
        return self.get(Medium, Medium.name, name)

    def get_medium_by_file_name(self, file_name: str) -> Medium:
        '''Get a medium by its file name. Returns None if not registered.'''
        return self.get(Medium, Medium.file_name, file_name)

    def get_medium_by_id(self, id: int) -> Medium:
        '''Get a medium by its id. Returns None if not registered.'''
        return self.get(Medium, Medium.id, id)

    def create(self, model, commit: bool = True, **kwargs):
        '''Base create method'''
        instance = model(**kwargs)
        self.add(instance)

        if commit:
            self.commit()

        return instance

    def create_user(self, tg_id: int, level: int | Levels = Levels.BASIC, commit: bool = True, **kwargs) -> User:
        '''Create a new user'''
        return self.create(User, tg_id=tg_id, level=level, commit=commit, **kwargs)

    def create_chat(self, tg_id: int, level: int | Levels = Levels.BASIC, commit: bool = True, **kwargs) -> Chat:
        '''Create a new chat'''
        return self.create(Chat, tg_id=tg_id, level=level, commit=commit, **kwargs)

    def create_command(self, name: str, level: int | Levels = Levels.BASIC, description: str | None = None, show: bool = True, commit: bool = True, **kwargs) -> Command:
        '''Create a new command'''
        return self.create(Command, name=name, description=description, level=level, show=show, commit=commit, **kwargs)

    def create_medium(self, media_type: str | Medium.Types, file_name: str, name: str | None = None, commit: bool = True, **kwargs) -> Medium:
        '''Create a new medium'''
        return self.create(Medium, media_type=media_type, file_name=file_name, name=name, commit=commit, **kwargs)

    def delete_media(self, types: Medium.Types | tuple[Medium.Types] | None = None, commit: bool = True):
        types = ([types] if type(types) == Medium.Types else types) if types else tuple(t.value for t in Medium.Types)

        for t in types:
            self.execute(delete(Medium).where(Medium.type == t))
        
        if commit:
            self.commit()


def load_data_session(database_path: str, absolute_path: bool = True, create_metadata: bool = False) -> DataSession:
    '''Create a DataSession instance using the data database file path'''
    engine = create_engine(f"sqlite://{"/" if absolute_path else ""}{database_path}")
    if create_metadata:
        Base.metadata.create_all(bind=engine)
    return DataSession(engine)

def create_data_session(database_path: str, absolute_path: bool = True) -> DataSession:
    return load_data_session(database_path, absolute_path, True)

if __name__ == "__main__":
    data = create_data_session("Data.db")
    data.create_user(124, Levels.OWNER)
    print(data.get_user(0))





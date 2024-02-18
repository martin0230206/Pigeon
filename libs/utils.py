from enum import IntEnum


class DescIntEnum(IntEnum):
    """ 定義一個有 description 屬性的整數枚舉類型

    REF:
        https://rednafi.com/python/add_attributes_to_enum_members/
    """
    # Declaring the additional attributes here keeps mypy happy.
    description: str

    def __new__(cls, code_int: int, description: str = "") -> 'DescIntEnum':
        obj = int.__new__(cls, code_int)
        obj._value_ = code_int
        obj.description = description
        return obj

    @classmethod
    def get_markdown_description(cls) -> str:
        """ 以 markdown 格式回傳 description
        """
        return (
            f"{cls.__doc__}\n\n"
            + "\n".join([
                f"- {statusIntEnum.value}: {statusIntEnum.description}"
                for statusIntEnum in cls
            ])
        )

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}.{self.name}: {self.value}, {self.description}>"

    def __repr__(self) -> str:
        return self.__str__()


class DescAliasIntEnum(IntEnum):
    """ 定義一個有 description、alias 屬性的整數枚舉類型

    REF:
        https://rednafi.com/python/add_attributes_to_enum_members/
    """
    # Declaring the additional attributes here keeps mypy happy.
    description: str
    alias: str

    def __new__(
        cls,
        code_int: int,
        description: str = "",
        alias: str = "",
    ) -> 'DescIntEnum':
        obj = int.__new__(cls, code_int)
        obj._value_ = code_int
        obj.description = description
        obj.alias = alias
        return obj

    @classmethod
    def get_markdown_description(cls) -> str:
        """ 以 markdown 格式回傳 description
        """
        return (
            f"{cls.__doc__}\n\n"
            + "\n".join([
                f"- {statusIntEnum.value}: {statusIntEnum.description} ({statusIntEnum.alias}))"
                for statusIntEnum in cls
            ])
        )

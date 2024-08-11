from abc import ABCMeta, abstractmethod


class ModelEnum(object, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def _valid_choices_list(cls):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def _choice_label_dict(cls):
        raise NotImplementedError()

    @classmethod
    def label_for(cls, key):
        try:
            return cls._choice_label_dict()[key]
        except KeyError:
            raise KeyError('{key} is not a valid value for {cls}'.format(key=key, cls=cls))

    @classmethod
    def choices(cls):
        return [(key, cls.label_for(key)) for key in cls._valid_choices_list()]

from typing import Union, Sequence, Dict, Type
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.'
                    )

    def get_message(self) -> str:
        """Строка сообщения"""
        return self.message.format(**asdict(self))

    def print_message(self) -> None:
        print(self.get_message())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance()
        speed: float = distance / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 20   
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        calories: float = (((
            self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed())
            - self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM
            * (self.duration * self.MIN_IN_HOUR))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self, action, duration, weight, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        speed_km_h: float = self.get_mean_speed()
        calories: float = ((
            self.COEFF_CALORIE_1 * self.weight
            + (speed_km_h ** 2 // self.height)
            * self.COEFF_CALORIE_2 * self.weight)
            * self.duration * self.MIN_IN_HOUR)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        speed: float = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories: float = (self.get_mean_speed() + self.COEFF_CALORIE_1) * \
            self.COEFF_CALORIE_2 * self.weight
        return calories


def read_package(workout_type: str, data: Sequence[int]) -> Union[
        Running, SportsWalking, Swimming]:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                 'RUN': Running,
                                                 'WLK': SportsWalking}
    if workout_type not in training_types:
        a = training_types.keys()
        b = ', '.join(a)
        raise KeyError(f'Тип тренировки должен быть {b}')
    return training_types[workout_type](*data)


def main(training: Union[Running, SportsWalking, Swimming]) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

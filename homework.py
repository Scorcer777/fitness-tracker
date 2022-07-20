from typing import Union, Sequence


class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration_h: float
    distance_km: float
    speed_km_h: float
    energy_spent: float

    def __init__(self, training_type: str, duration: float,
                 distance_km: float, speed_km_h: float,
                 energy_spent: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance_km = distance_km
        self.speed_km_h = speed_km_h
        self.energy_spent = energy_spent

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type};'
                        f'Длительность: {self.duration};'
                        f'Дистанция: {self.distance_km};'
                        f'Средняя скорость: {self.speed_km_h};'
                        f'Потрачено калорий: {self.energy_spent}'
                        )

        return message

    def print_message(self) -> None:
        print(self.get_message())


class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: float
    M_IN_KM: int

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
        LEN_STEP: float = 0.65
        M_IN_KM: float = 1000
        distance_km: float = self.action * LEN_STEP / M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance()
        speed_km_h: float = distance / self.duration
        return speed_km_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        duration = self.duration
        distance_km = self.get_distance()
        speed_km_h = self.get_mean_speed()
        energy_spent = self.get_spent_calories()

        return InfoMessage(self.__class__.__name__,
                           duration,
                           distance_km,
                           speed_km_h,
                           energy_spent
                           )


class Running(Training):
    coeff_calorie_1: int
    coeff_calorie_2: int
    M_IN_KM: int
    MIN_IN_HOUR: int
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        M_IN_KM: int = 1000
        speed: float = self.get_mean_speed()
        MIN_IN_HOUR: int = 60
        duration_minutes: float = self.duration * MIN_IN_HOUR
        energy_spent: float = (((coeff_calorie_1 * speed) - coeff_calorie_2)
                               * self.weight / M_IN_KM
                               * duration_minutes)
        return energy_spent


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    coeff_calorie_1: float
    coeff_calorie_2: float
    coeff_calorie_3: int
    MIN_IN_HOUR: int

    def __init__(self, action, duration, weight, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        coeff_calorie_3: int = 2
        speed: float = self.get_mean_speed()
        MIN_IN_HOUR: int = 60
        duration_minutes: float = self.duration * MIN_IN_HOUR
        energy_spent: float = ((
            coeff_calorie_1 * self.weight
            + (speed ** coeff_calorie_3 // self.height)
            * coeff_calorie_2 * self.weight) * duration_minutes)
        return energy_spent


class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int
    M_IN_KM: int
    coeff_calorie_1: float
    coeff_calorie_2: int

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        M_IN_KM: int = 1000
        speed_km_h: float = (
            self.length_pool * self.count_pool / M_IN_KM / self.duration)
        return speed_km_h

    def get_spent_calories(self) -> float:
        speed_km_h: float = self.get_mean_speed()
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        energy_spent = (speed_km_h + coeff_calorie_1) * \
            coeff_calorie_2 * self.weight
        return energy_spent


def read_package(workout_type: str, data: Sequence[int]) -> Union[
        Running, SportsWalking, Swimming]:
    """Прочитать данные полученные от датчиков."""
    training_types = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking
                      }
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

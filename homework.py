from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Класс {type(self).__name__} не содержит'
                                  'метод get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())

#нужно ли использовать декоратор в дочерних классах?
class Running(Training):
    """Тренировка: бег."""
    COEF_CALORIE_RUN_1 = 18
    COEF_CALORIE_RUN_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEF_CALORIE_RUN_1 * self.get_mean_speed()
                - self.COEF_CALORIE_RUN_2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # конструктор принимает доп параметр - рост спортсмена
    COEF_CALORIE_WLK_1 = 0.035
    COEF_CALORIE_WLK_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEF_CALORIE_WLK_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEF_CALORIE_WLK_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    # кроме свойство базового класса принимает еще два параметра
    # переопределить расчет калорий и расчет ср. скорости

    COEF_CALORIE_SWM_1 = 1.1
    COEF_CALORIE_SWM_2 = 2.0
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    # переопределяем метод расчета калорий и метод расчета средней скорости
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEF_CALORIE_SWM_1)
                * self.COEF_CALORIE_SWM_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking}
    if workout_type not in train:
        raise ValueError(f'Тренировка {workout_type} не поддерживается :(')
    return train[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
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

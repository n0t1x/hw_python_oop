class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                training_type: str,
                duration: float,
                distance: float,
                speed: float,
                calories: float
                ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return f'Тип тренировки: {self.training_type}; Длительность: {self.duration} ч.; Дистанция: {self.distance} км; Ср. скорость: {self.speed} км/ч; Потрачено ккал: {self.calories}.'
    
    #def show_training_info() -> None:
    #  pass


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance 

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    # переопределим метод расчета калорий, остальные свойства и методы наследуются без изменений
    
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.coeff_calorie_1 * self.get_mean_speed()
                 - self.coeff_calorie_2) * self.weigth / self.M_IN_KM
                 * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # конструктор принимает доп параметр - рост спортсмена
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029

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
        return (self.coeff_calorie_1 * self.weigth + (self.mean_speed ** 2 // self.height) * self.coeff_calorie_2 * self.weigth) * self.duration 


class Swimming(Training):
    """Тренировка: плавание."""
    # кроме свойство базового класса принимает еще два параметра
    SWM_coeff_calorie_1: float = 1.1
    SWM_coeff_calorie_2: float = 2.0
    LEN_STEP: float = 1.38

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
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + self.SWM_coeff_calorie_1) * self.SWM_coeff_calorie_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train = {
        "SWM":Swimming,
        "RUN":Running,
        "WLK":SportsWalking}
    train_obj = train[workout_type](*data)
    return train_obj


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



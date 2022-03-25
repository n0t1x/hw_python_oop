class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                training_type: str,
                duration: float,
                distance: float,
                speed: float,
                calories: float
                ) -> None:
        pass

    def get_message(self) -> None:
        return f'Тип тренировки: {training_type}; Длительность: {duration} ч.; Дистанция: {distance} км; Ср. скорость: {speed} км/ч; Потрачено ккал: {calories}.'
    
    def show_training_info() -> None:

        pass


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    LEN_SMW = 1.38
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        pass

    def get_distance(self, action: int) -> float:
        """Получить дистанцию в км."""
        distance = action * LEN_STEP / M_IN_KM
        return distance 

    def get_mean_speed(self, distance: float, duration: float) -> float:
        """Получить среднюю скорость движения."""
        return distance / duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""
    # переопределим метод расчета калорий, остальные свойства и методы наследуются без изменений
    
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self, mean_speed: float, weigth: float, duration: float) -> float:
        """Получить количество затраченных калорий."""
        return (coeff_calorie_1 * mean_speed - coeff_calorie_2) * weigth / M_IN_KM * duration 


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

    def get_spent_calories(self, mean_speed: float, weigth: float, duration: float) -> float:
        """Получить количество затраченных калорий."""
        return (coeff_calorie_1 * weigth + (mean_speed ** 2 // height) * coeff_calorie_2 * weigth) * duration 


class Swimming(Training):
    """Тренировка: плавание."""
    # кроме свойство базового класса принимает еще два параметра

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None: 
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    # переопределяем метод расчета калорий и метод расчета средней скорости
    def get_mean_speed(self, distance: float, duration: float, length_pool: float) -> float:
        """Получить среднюю скорость плавания."""
        return length_pool * count_pool / M_IN_KM / duration

    def get_spent_calories(self, mean_speed: float, weight: float) -> float:
        """Получить количество затраченных калорий."""
        return (mean_speed + 1.1) * 2 * weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    code: set = {
            "SWM":Swimming(data[0], data[1], data[2], data[3], data[4]),
            "RUN":Running(data[0], data[1], data[2]),
            "WLK":SportsWalking(data[0], data[1], data[2], data[3])
            }
    train_obj = code.get(workout_type)
    return train_obj


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info.print_message(info.get_message())
    

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)



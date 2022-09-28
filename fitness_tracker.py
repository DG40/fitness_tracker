# КЛАСС ОБЪЕКТОВ СООБЩЕНИЙ (объекты создаются из метода show_training_info() класса Training):
class InfoMessage:
    """Информационное сообщение о тренировке:"""
    training_type = None
    duration = None
    distance = None
    speed = None
    calories = None

    def get_message(self) -> str:  # Метод для формирования сообщения, которое потом будет выводиться на экран из Main
        message = 'Тип тренировки: ' + str(self.training_type) + '; ' \
            'Длительность: ' + str(self.duration) + '; Дистанция: ' + str(self.distance) \
            + '; Средняя скорость: ' + str(self.speed) + \
            '; Расход энергии: ' + str(self.calories) + ';'
        return message


# БАЗОВЫЙ КЛАСС "ТРЕНИРОВКА":
class Training:
    """Базовый класс тренировки:"""

    # Атрибут данных (переменная класса), общий для всех экземпляров класса:
    M_IN_KM = 1000  # (константа для перевода значений из метров в километры)

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action  # Количество шагов / гребков
        self.duration = duration  # Длительность тренировки
        self.weight = weight  # Вес спортсмена
        self.LEN_STEP = None  # Не определена, пока не ясен вид тренировки

    def get_distance(self) -> float:  # Получить дистанцию в км:
        return round(self.action * self.LEN_STEP / self.M_IN_KM, 3)  # (округляем до тысячных)

    def get_mean_speed(self) -> float:  # Получить среднюю скорость движения:
        return round(self.get_distance() / self.duration, 3)  # (округляем до тысячных)

    def get_spent_calories(self) -> float:  # Получить количество затраченных калорий:
        # В каждом виде тренировок рассчитывается по-своему, поэтому пока используем заглушку pass:
        pass

    def show_training_info(self) -> InfoMessage:  # Формируем объект класса InfoMessage о выполненной тренировке:
        # Создаём объект класса InfoMessage():
        msg = InfoMessage()
        # Определяем свойства, общие для всех типов тренировок:
        msg.duration = self.duration
        msg.distance = self.get_distance()
        # Определяем остальные свойства, частные для каждого типа тренировки:
        if isinstance(self, Running):  # - для бега:
            msg.training_type = 'Running'
            msg.speed = self.get_mean_speed()
            msg.calories = Running.get_spent_calories(self)
        elif isinstance(self, SportsWalking):  # - для спортивной ходьбы:
            msg.training_type = 'SportsWalking'
            msg.speed = self.get_mean_speed()
            msg.calories = SportsWalking.get_spent_calories(self)
        elif isinstance(self, Swimming):  # - для плавания:
            msg.training_type = 'Swimming'
            msg.speed = Swimming.get_mean_speed(self)
            msg.calories = Swimming.get_spent_calories(self)

        return msg


# КЛАСС "БЕГ":
class Running(Training):
    """Тренировка: бег:"""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        Training.__init__(self, action, duration, weight)
        self.LEN_STEP = 0.65  # - переопределяем: длина шага во время бега

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий:"""
        coef_calorie_1 = 18  # - вынесли неименованный коэффициент в переменную
        coef_calorie_2 = 20  # - вынесли неименованный коэффициент в переменную

        return round((coef_calorie_1 * self.get_mean_speed() -
                      coef_calorie_2) * self.weight / self.M_IN_KM * self.duration * 60, 3)  # (округляем до тысячных)


# КЛАСС "СПОРТИВНАЯ ХОДЬБА":
class SportsWalking(Training):
    """Тренировка: спортивная ходьба:"""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        Training.__init__(self, action, duration, weight)
        self.LEN_STEP = 0.65  # - переопределяем: длина шага во спортивной ходьбы
        self.height = height

    def get_spent_calories(self) -> float:  # - переопределяем метод базового класса для расчёта калорий:
        """Получить количество затраченных калорий:"""
        coef_calorie_walk_1 = 0.035
        coef_calorie_walk_2 = 0.029

        return round((coef_calorie_walk_1 * self.weight + ((self.get_mean_speed()) ** 2 // self.height)
                      * coef_calorie_walk_2 * self.weight) * self.duration * 60, 3)  # (округляем до тысячных)


# КЛАСС "ПЛАВАНИЕ":
class Swimming(Training):
    """Тренировка: плавание:"""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        Training.__init__(self, action, duration, weight)
        self.LEN_STEP = 1.38  # - переопределяем: длина гребка
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:  # - переопределяем метод базового класса для расчёта средней скорости:
        """Получить среднюю скорость движения:"""
        return round(self.length_pool * self.count_pool / self.M_IN_KM / self.duration, 3)  # (округляем до тысячных)

    def get_spent_calories(self) -> float:  # - переопределяем метод базового класса для расчёта калорий:
        """Получить количество затраченных калорий:"""
        coef_calorie_swim = 1.1  # - вынесли неименованный коэффициент в переменную
        return round((self.get_mean_speed() + coef_calorie_swim) * 2 * self.weight, 3)  # (округляем до тысячных)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков:"""
    # Создаём вспомогательный словарь
    # (коду тренировки сопоставляется класс, который нужно вызвать для каждого типа тренировки):
    training_vocabulary = {'RUN': Running, 'WLK': SportsWalking, 'SWM': Swimming}
    test_obj = training_vocabulary[workout_type](*data)  # - создали объект, соответствующий типу анализируемой
    # тренировки (по этому объекту будет производиться анализ данных и вывод результатов)
    return test_obj


def main(training: Training) -> None:
    """Главная функция:"""
    # Формируем объект класса InfoMessage о выполненной тренировке:
    info = Training.show_training_info(training)  # - объект класса InfoMessage с набором свойств
    # Формируем из него сообщение с данными о тренировке:
    answer = InfoMessage.get_message(info)  # - объект типа String
    print(answer)


if __name__ == '__main__':  # (выполняется только в случае, если этот файл запущен как самостоятельная программа)
    packages = [  # - тестовые данные:
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:  # В первой итерации будет: workout_type = SWM; data = [720, 1, 80, 25, 40]
        training = read_package(workout_type, data)  # - создаётся объект класса, соответствующего типу тренировки
        main(training)  # - берём объект тренировки в работу Main

import cv2
from time import sleep


#1 задание 4 вариант
def task_1():
    image = cv2.imread('variant-4.jpeg') # Загрузка изображения
    b_ch, g_ch, r_ch = cv2.split(image) # Разделение изображения на отдельные каналы
    # Создание нового изображения, где зеленый и красный каналы равны 0
    blue_img = cv2.merge((b_ch, g_ch * 0, r_ch * 0))
    # Отображение только синего канала
    cv2.imshow('Blue Channel', blue_img)


#2 задание
def task_2():
    # подключаемся к камере
    cap = cv2.VideoCapture(0)
    resolution = (640, 480)
    # середина экрана относительно горизонтали
    middle_x = resolution[0] // 2
    for tick in range(120):
        sleep(0.5)  #устанавливаем время
        # читаем фрейм
        ret, frame = cap.read()
        if not ret:
            continue  # повтор при некорректной попытке

        # приводим изображение к используемому разрешению
        frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_LINEAR)
        # ищем метку по контурам в оттенках серого
        gray = cv2.GaussianBlur(
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
            (21, 21), 0
        )
        thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)[1]
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
        # если контур(-ы) найдены
        if len(contours):
            # выбираем наибольший по площади
            c = max(contours, key=cv2.contourArea)
            # запоминаем размеры
            x, y, w, h = cv2.boundingRect(c)
            # если центр метки правее середины экрана
            if x + (w // 2) > middle_x:
                # выводим текст
                cv2.putText(
                    frame, 'МЕТКА СПРАВА!', (middle_x, 20), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2, 2
                )

        # показываем результирующий фрейм
        cv2.imshow('Cam', frame)
    # отключаемся от камеры
    cap.release()


if __name__ == '__main__':
    task_1()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    task_2()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

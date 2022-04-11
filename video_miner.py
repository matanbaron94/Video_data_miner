import time
import cv2
from pynput.mouse import Controller
import keyboard
import os
import ctypes


def main():

    #-------------------- Adjustments ----------------------#



    # Name the object
    object_name = "object name"

    # Path to database dir  - here the data will be saved
    path_to_data_dir = rf"data\{object_name}"

    # Path to video
    video = "docs/rd.mp4"

    webcam = False

    # The size of the images to be saved
    saved_img_size = 200

    #resolution vector
    rs = 3

    # -------------------------------------------------------#


    if webcam == True:
        video = 0
        rs= 1



    machine = ctypes.windll.user32
    mouse = Controller()




    cap = cv2.VideoCapture(video)
    r, frame = cap.read()
    v = frame.shape
    print(v)
    resolution = (int(v[1]/rs), int(v[0]/rs))


    # Colors
    green_color = [0, 255, 0]
    blue_color = [255, 0, 0]
    red_color = [0, 0, 255]


    # Modes
    record = False
    freeze = False
    lock = False


    # Other variables
    crop = 1
    pic_counter = 1
    x_lock = 0
    y_lock = 0
    speed = 0

    retangle_size=200
    retangle_radius = int(retangle_size/2)


    # Screen position variables
    screen_w = machine.GetSystemMetrics(0)
    screen_h = machine.GetSystemMetrics(1)
    print(screen_w)
    padding_top = int(screen_h/2 - (resolution[1]))
    padding_left = int(screen_w/2 - (resolution[0])- (resolution[1]/2))
    space = 2


    # craete dir for the data
    if os.path.exists(path_to_data_dir):
        pass
    else:
        os.makedirs(path_to_data_dir)
    os.chdir(path_to_data_dir)


    # getting the shpe of the original farme
    r, frame = cap.read()
    v = frame.shape
    print(v)
    v = int(v[1] / resolution[0])


    # positioning the main video
    cv2.namedWindow("Original")
    cv2.moveWindow('Original', padding_left + 350 +space, padding_top)




# ---------------------------------- main loop -------------------------------------- #

    while True:

        retangle_x = 0
        retangle_y = 0


        # Getting mouse position
        mouse_x, mouse_y = mouse.position
        mouse_x = int(mouse_x)
        mouse_y = int(mouse_y)



        # --------------- Setup keyboard ------------------#

        # Press '+' to speed up
        if keyboard.is_pressed('+'):
            speed = speed + 0.001

        # Press '-' to slow down
        if keyboard.is_pressed('-'):
            speed = speed - 0.001

        # Press 'S' to zoom out
        if keyboard.is_pressed('s'):
            retangle_size= int(retangle_size+5)
            retangle_radius = int(retangle_size/2)
            crop = crop -0.05

        # Press 'w' to zoon in
        if keyboard.is_pressed('w'):
            retangle_size= int(retangle_size-5)
            retangle_radius = int(retangle_size / 2)
            crop = crop +0.05

        # Press 'space' to puse the video
        if keyboard.is_pressed('space') is True and freeze is False:
            freeze = True
            time.sleep(0.05)
            keyboard.release('space')
            time.sleep(0.1)
        if keyboard.is_pressed('space') is True and freeze is True:
            freeze = False
            time.sleep(0.05)
            keyboard.release('space')
            time.sleep(0.1)

        #Press 'R' to start mineing
        if keyboard.is_pressed('r') is True and record is False:
            record = True
            time.sleep(0.05)
            keyboard.release('r')
            time.sleep(0.1)
        if keyboard.is_pressed('r') is True and record is True:
            record = False
            time.sleep(0.05)
            keyboard.release('r')
            time.sleep(0.1)


        # Press 'L' to lock on target
        if keyboard.is_pressed('l') and lock is False:
            lock = True
            time.sleep(0.05)
            keyboard.release('l')
            time.sleep(0.1)
        if keyboard.is_pressed('l') and lock is True:
            lock = False
            time.sleep(0.05)
            keyboard.release('l')
            time.sleep(0.1)





        # ---------------------Frames-------------------------- #

        if freeze == False:
            success, frame = cap.read()


        # Setup frames to work
        crop_frame = frame.copy()
        original_frame = frame.copy()
        original_frame = cv2.resize(original_frame, resolution)





        # ---------------- Positioning the retangle sight -------------------- #

        original_pos = cv2.getWindowImageRect("Original")
        original_pos_x = original_pos[0]
        original_pos_y = original_pos[1]


        if retangle_size <20:
            retangle_size = 20
            retangle_radius = 10
            print("dfgfdgdfgdfg")

        if retangle_size > resolution[1]:
            retangle_size = resolution[1]


        if mouse_x > (original_pos_x +retangle_radius):
            retangle_x = mouse_x - original_pos_x- retangle_radius

        if mouse_x > original_pos_x + resolution[0] - retangle_radius:
            retangle_x = resolution[0] -retangle_size


        if mouse_y > (original_pos_y + retangle_radius):
            retangle_y = mouse_y - original_pos_y - retangle_radius

        if mouse_y > original_pos_y + resolution[1] - retangle_radius:
            retangle_y = resolution[1] -retangle_size





        # ---------------------Modes------------------------- #

        # On unlock mode
        if lock == False:
            cv2.rectangle(original_frame, (retangle_x, retangle_y), (retangle_x + retangle_size, retangle_y + retangle_size), green_color, 2, )
            x_lock = retangle_x
            y_lock = retangle_y

        # on lock mode
        if lock == True:
            retangle_x = x_lock
            retangle_y = y_lock
            cv2.rectangle(original_frame, (retangle_x, retangle_y), (retangle_x + retangle_size, retangle_y + retangle_size), blue_color, 2, )

        crop_frame = crop_frame[retangle_y*v:retangle_y*v +retangle_size*v , retangle_x*v:retangle_x*v+retangle_size*v]
        crop_frame = cv2.resize(crop_frame, (resolution[1], resolution[1]))

        # On record mode
        if record == True:
            cv2.rectangle(original_frame, (retangle_x, retangle_y),(retangle_x + retangle_size, retangle_y + retangle_size), red_color, 2, )
            cv2.circle(original_frame, (30, 40), 10, red_color, -1, )
            file_name = f"img_{pic_counter}.jpg"
            img_to_save = crop_frame.copy()
            img_to_save= cv2.resize(img_to_save, (saved_img_size,saved_img_size))
            cv2.imwrite(file_name, img_to_save)
            print(pic_counter)
            pic_counter+=1


        # Setup speed
        if speed <=0:
            speed = 0
        time.sleep(speed)
        original_frame = cv2.putText(original_frame, f"x{1-(10*speed)}", (20,20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, green_color, 1, cv2.LINE_AA)


        # ---------------------Imshow------------------------- #

        cv2.imshow('Original', original_frame)
        cv2.imshow('Crop image', crop_frame)
        cv2.moveWindow('Crop image', original_pos_x +resolution[0], original_pos_y-30)



        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

main()
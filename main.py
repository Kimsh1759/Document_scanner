import pygame, sys
import cv2
from pygame.locals import *
from button import Button
from webcam import Webcam
import tensorflow as tf
import numpy as np
from PIL import Image

pygame.init()

WIDTH = 1800
HEIGHT = 900

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
menuBG = pygame.image.load("scanner\image\mainBG.PNG")
menuBG = pygame.transform.scale(menuBG, (WIDTH, HEIGHT))
camera = pygame.image.load("scanner\image\camera.PNG")
camera = pygame.transform.scale(camera, (200, 150))
cameraBG = pygame.image.load("scanner\image\cameraBG.PNG")
cameraBG = pygame.transform.scale(cameraBG, (660, 500))
captureBG = pygame.image.load("scanner\image\capture.PNG")
captureBG = pygame.transform.scale(captureBG, (150, 150))
pygame.display.set_caption("CAPTURE PROGRAM")

fps_clock = pygame.time.Clock()
capture = cv2.VideoCapture("http://192.168.0.251:4747/video")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("scanner/NanumBarunpenR.ttf", size)


def main_menu():
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.update()
    while True:
        SCREEN.blit(menuBG, (0, 0))
        SCREEN.blit(camera, (770, 150))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        START_BUTTON = Button(
            image=None,
            pos=(870, 550),
            text_input="START",
            font=get_font(50),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        QUIT_BUTTON = Button(
            image=None,
            pos=(870, 700),
            text_input="QUIT",
            font=get_font(50),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        for button in [START_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    cam_screen()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def scan_image_getSize(scan_cam):
    w, h, _ = scan_cam.shape
    width = 1120 - (h / 2)
    height = 290 - (w / 2)
    return width, height


def cam_screen():
    LODING_TEXT = get_font(60).render("잠시만 기다려 주세요", True, "white")
    LODING_TEXT_loc = LODING_TEXT.get_rect(center=(850, 160))
    CAM_TEXT = get_font(30).render(" CAM ", True, "white")
    CAM_TEXT_loc = CAM_TEXT.get_rect(center=(360, 565))
    CAP_TEXT = get_font(30).render("미리보기", True, "white")
    CAP_TEXT_loc = CAP_TEXT.get_rect(center=(1120, 565))
    SCREEN.blit(menuBG, (0, 0))
    SCREEN.blit(LODING_TEXT, LODING_TEXT_loc)
    pygame.display.update()

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        QUIT_BUTTON = Button(
            image=None,
            pos=(1720, 60),
            text_input="QUIT",
            font=get_font(30),
            base_color="#d7fcd4",
            hovering_color="black",
        )
        CAP_BUTTON = Button(
            image=captureBG,
            pos=(750, 700),
            text_input="촬영",
            font=get_font(20),
            base_color="#d7fcd4",
            hovering_color="black",
        )
        SCREEN.blit(menuBG, (0, 0))
        SCREEN.blit(cameraBG, (40, 40))
        SCREEN.blit(cameraBG, (790, 40))
        SCREEN.blit(CAM_TEXT, CAM_TEXT_loc)
        SCREEN.blit(CAP_TEXT, CAP_TEXT_loc)
        for button in [CAP_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        status, frame = capture.read()
        pts, scan = Webcam.webcam_scan(frame)
        cam = cvimage_to_pygame(scan)
        try:
            scan_cam = Webcam.scan_docs(pts, frame)
            scan_cam_p = cvimage_to_pygame(scan_cam)
            SCREEN.blit(scan_cam_p, scan_image_getSize(scan_cam))
        except:
            print()
        SCREEN.blit(cam, (50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if CAP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    capture_screen(scan_cam)

        pygame.display.update()
        fps_clock.tick(100)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()


def capture_screen(scan_cam):
    screen_h, screen_w, _ = scan_cam.shape
    pScan_cam = cvimage_to_pygame(scan_cam)
    cSCREEN = pygame.display.set_mode((int(screen_h) + 30, int(screen_w) + 70))
    captureScreenBG = pygame.image.load("scanner\image\catureScreenBG.PNG")
    captureScreenBG = pygame.transform.scale(
        captureScreenBG, (int(screen_h) + 30, int(screen_w) + 70)
    )
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        cSCREEN.blit(captureScreenBG, (0, 0))
        cSCREEN.blit(pScan_cam, (15, 15))
        QUIT_BUTTON = Button(
            image=None,
            pos=(45, screen_w + 55),
            text_input="나가기",
            font=get_font(20),
            base_color="#d7fcd4",
            hovering_color="black",
        )
        SAVE_BUTTON = Button(
            image=None,
            pos=(screen_h - 15, screen_w + 55),
            text_input="저장",
            font=get_font(20),
            base_color="#d7fcd4",
            hovering_color="black",
        )
        for button in [SAVE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                if SAVE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    cv2.imwrite("save.jpg", scan_cam)
        pygame.display.update()


def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "BGR")


if __name__ == "__main__":
    main_menu()
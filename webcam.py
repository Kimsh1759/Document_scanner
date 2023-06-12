import cv2
import numpy as np


class Webcam:
    def scan_docs(pts, frame):
        sm = pts.sum(axis=1)
        diff = np.diff(pts, axis=1)

        topLeft = pts[np.argmin(sm)]
        bottomRight = pts[np.argmax(sm)]
        topRight = pts[np.argmin(diff)]
        bottomLeft = pts[np.argmax(diff)]

        pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])

        w1 = abs(bottomRight[0] - bottomLeft[0])
        w2 = abs(topRight[0] - topLeft[0])
        h1 = abs(topRight[1] - bottomRight[1])
        h2 = abs(topLeft[1] - bottomLeft[1])
        width = max([w1, w2])
        height = max([h1, h2])

        pts2 = np.float32(
            [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]]
        )

        mtrx = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(frame, mtrx, (width, height))
        # sr = cv2.dnn_superres.DnnSuperResImpl_create()
        # sr.readModel("ESPCN_x4.pb")
        # sr.setModel("espcn", 4)
        # result1 = sr.upsample(result)
        return result

    def webcam_scan(frame):
        draw = frame.copy()
        gray = cv2.cvtColor(draw, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        edged = cv2.Canny(gray, 60, 400)
        cnts, _ = cv2.findContours(
            edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        flag = 0
        for c in cnts:
            peri = cv2.arcLength(c, True)
            verticles = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(verticles) == 4:
                cv2.drawContours(draw, cnts[flag], -1, (0, 255, 0), 3)
                break
            flag += 1
        try:
            pts = verticles.reshape(4, 2)
            for x, y in pts:
                cv2.circle(draw, (x, y), 10, (0, 0, 255), -1)
                return pts, draw
        except:
            return _, frame
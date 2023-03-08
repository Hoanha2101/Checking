import face_recognition as fr 
import cv2 as cv
import os
import shutil
import csv
import time
from unidecode import unidecode
import pandas as pd

#Note
# Column csv:  Id_No    Name    Age     Phone_number    Career      Checked_Count


def count_line_csv():
    with open('people_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = [row for row in reader]
    num_rows = int(len(data))
    return num_rows

def delete_image():
    file_path = "people_check\check_image.jpg" # đường dẫn tới file ảnh cần xóa

    if os.path.exists(file_path):
        os.remove(file_path)
    

def copy_image():
    file_path = "people_check\check_image.jpg"
    file_path_dst = "people_checked\check_image.jpg"
    shutil.copy(file_path, file_path_dst)

def take_photo():
    # Thiết lập đường dẫn thư mục để lưu ảnh
    path = 'people_check/'

    # Kiểm tra xem thư mục có tồn tại không, nếu không thì tạo mới
    if not os.path.exists(path):
        os.makedirs(path)

    # Thiết lập thiết bị camera mặc định
    cap = cv.VideoCapture(0)

    # Đợi camera được khởi động
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    # Chụp ảnh
    ret, frame = cap.read()

    # Hiển thị ảnh chụp được
    cv.imshow("Image", frame)

    # Nhập tên cho ảnh và lưu nó vào thư mục đã thiết lập
    # name = input("Nhập tên cho ảnh: ")
    name = "check_image"
    filename = os.path.join(path, name + ".jpg")
    cv.imwrite(filename, frame)

    # Thoát khỏi chương trình
    cap.release()
    cv.destroyAllWindows()
    
#********* Chụp ảnh
take_photo()
#*********

def load_target_image():
    load_image = "people_check\check_image.jpg"
    target_image = fr.load_image_file(load_image)
    target_encoding = fr.face_encodings(target_image)
    
    return target_image,target_encoding

def encode_faces(folder):
    list_people_encoding = []
    
    for filename in os.listdir(folder):
        known_image = fr.load_image_file(f'{folder}{filename}')
        known_encoding = fr.face_encodings(known_image)[0]
        
        list_people_encoding.append((known_encoding,filename))
    
    return list_people_encoding

def find_target_face(target_image = load_target_image()[0], target_encoding = load_target_image()[1]):
    face_location = fr.face_locations(target_image)
    if len(face_location) == 0:
        print("No person, try again!")
        delete_image()
        exit()
    if len(face_location) > 1:
        print("At the same time, only one person can check!")
        delete_image()
        exit()
    count_person_zero = 0
    is_target_face_list = []
    
    for person in encode_faces("people_checked/"):
        encoded_faces = person[0]
        filename = person[1]
        
        is_target_face = fr.compare_faces(encoded_faces, target_encoding, tolerance = 0.5)
        print(f"{is_target_face} {filename}")
        if is_target_face == [True]:
            is_target_face_list.append(True)
            id_no_extract = int(filename[0])
            with open("people_data.csv",newline="",encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                row_id_no_extract = None
                for i, row in enumerate(reader):
                    if i == (id_no_extract-1):
                        row_id_no_extract = row
                        break
                if row_id_no_extract is not None:
                    print(row_id_no_extract[1],"\nRất vui khi được gặp lại bạn tại đại học FPT Quy Nhơn")
                    row_id_no_extract[5] = int(int(row_id_no_extract[5]) + 1)
                    print("Hôm nay là lần thứ",row_id_no_extract[5],"bạn đến với ngôi trường này.")
            
            with open('people_data.csv', mode='r', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
            rows[id_no_extract-1][5] = row_id_no_extract[5]
            
            with open('people_data.csv', mode='w', newline='',encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
    
        # if face_location:
        #     face_number = 0
        #     for location in face_location:
        #         if is_target_face[face_number]:
        #             label = filename
        #             create_frame(location, label[2:-4])
                
        #     face_number = face_number + 1
            

    if count_person_zero == len(is_target_face_list):
        print("Chào mừng bạn đến với Đại học FPT Quy Nhơn")
        time.sleep(2)
        print("Please checking...")
        number_id = count_line_csv()
        name = str(input("Hãy nhập tên của bạn: "))
        age = int(input("Tuổi của bạn: "))
        phone_no = str(input("Số điện thoại của bạn: "))
        career = int(input("Ngành học mà bạn quan tâm:\n 1. Trí tuệ nhân tạo\n 2. Marketing\n 3. Kĩ thuật phần mềm\n 4. Kinh doanh quốc tế\n Lựa chọn của bạn: "))
        checked_count = int(1)
        
        if career == 1:
            career_content = "Trí tuệ nhân tạo"
        elif career == 2:
            career_content = "Marketing"
        elif career == 3:
            career_content = "Kĩ thuật phần mềm"
        else:
            career_content = "Kinh doanh quốc tế"
        
        with open('people_data.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(list([number_id + 1, name, age, phone_no, career_content,checked_count]))
            
        
        copy_image()
        name_handle = unidecode(name).replace(" ", "").lower()
        current_name = "people_checked\check_image.jpg"
        new_name = "people_checked\\"+ str((number_id + 1)) +"_"+ name_handle +".jpg"
        os.rename(current_name,new_name)
        delete_image()
        
        print("....Cảm ơn....")
        
        
# def create_frame(location, label):
#     top, right, bottom, left = location
#     cv.rectangle(load_target_image()[0],(left, top), (right, bottom),(255,0,0), 2)
#     cv.putText(load_target_image()[0],label,(left + 3, top - 14),cv.FONT_HERSHEY_DUPLEX,0.4,(255,255,255,1))

def render_image(target_image = load_target_image()[0]):
    rgb_img = cv.cvtColor(target_image, cv.COLOR_BGR2RGB)  
    cv.imshow("Face Recognition", rgb_img)
    cv.waitKey(0)
    

find_target_face()
render_image()
delete_image()

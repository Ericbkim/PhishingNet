from home import read_img

img1 = 'test_img_comp/test_email_1_1.jpg'
img2 = 'test_img_comp/test_email_2_1.jpg'
img3 = 'test_img_comp/test_email_3_1.jpg'

img1_text = read_img.get_img_text(img1)
img2_text = read_img.get_img_text(img2)
img3_text = read_img.get_img_text(img3)

print("Text from img1:")
print(img1_text)
print("Text from img2")
print(img2_text)
print("Text from img3")
print(img3_text)

print("Cosine similarity of test_email_1_1.jpg with itself is: {}".format(read_img.get_text_comp(img1_text, img1_text)))
print("Cosine similarity of test_email_1_1.jpg with test_email_2_1 is: {}".format(read_img.get_text_comp(img1_text, img2_text)))
print("Cosine similarity of test_email_1_1.jpg with test_email_3_1 is: {}".format(read_img.get_text_comp(img1_text, img3_text)))
print("Cosine similarity of test_email_2_1.jpg with test_email_3_1 is: {}".format(read_img.get_text_comp(img2_text, img3_text)))

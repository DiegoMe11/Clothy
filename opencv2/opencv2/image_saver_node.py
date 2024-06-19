import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy
from cv_bridge import CvBridge
import cv2
import os
import numpy as np
import tensorflow as tf
from PIL import Image as PILImage

# TensorFlow and Keras setup
img_width, img_height = 150, 150
train_data_dir = '/home/cmarrod3/Desktop/dataset/train'
validation_data_dir = '/home/cmarrod3/Desktop/dataset/validation'
batch_size = 16
epochs = 1

# Data generators
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary'
)

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary'
)

# Model construction
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 3)),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Model compilation
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Model training
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)

# Load and predict function
def load_and_predict(image_path):
    img = PILImage.open(image_path)
    img = img.resize((img_width, img_height))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    return prediction[0][0]

# Detect color function
def detect_color(hsv_img, lower, upper, color_name, original_img):
    mask = cv2.inRange(hsv_img, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    total_pixels = np.sum(mask > 0)
    
    max_area = 0
    max_contour = None
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour
    
    if max_contour is not None:
        x, y, w, h = cv2.boundingRect(max_contour)
        cv2.rectangle(original_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(original_img, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return total_pixels, original_img

# ImageSaver node
class ImageSaver(Node):
    def __init__(self):
        super().__init__('image_saver_node')
        self.bridge = CvBridge()

        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            depth=10,
            durability=QoSDurabilityPolicy.VOLATILE
        )

        self.image_sub = self.create_subscription(
            Image,
            '/image',
            self.image_callback,
            qos_profile
        )

        self.save_dir = os.path.expanduser('~/Desktop')
        self.image_saved = False
        self.latest_image = None
        self.get_logger().info(f'Image saver node started. Images will be saved to {self.save_dir}')

    def image_callback(self, msg):
        if not self.image_saved:
            try:
                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
                
                lower_blue = np.array([110, 50, 50])
                upper_blue = np.array([130, 255, 255])
                lower_red = np.array([170, 50, 50])
                upper_red = np.array([180, 255, 255])
                lower_yellow = np.array([20, 100, 100])
                upper_yellow = np.array([30, 255, 255])
                lower_green = np.array([30, 50, 50])
                upper_green = np.array([90, 255, 255])
                
                colors = {
                    'Azul': detect_color(hsv, lower_blue, upper_blue, 'Azul', cv_image.copy()),
                    'Rojo': detect_color(hsv, lower_red, upper_red, 'Rojo', cv_image.copy()),
                    'Amarillo': detect_color(hsv, lower_yellow, upper_yellow, 'Amarillo', cv_image.copy()),
                    'Verde': detect_color(hsv, lower_green, upper_green, 'Verde', cv_image.copy()),
                }
                
                max_color = max(colors, key=lambda k: colors[k][0])
                
                save_path = os.path.join(self.save_dir, f'fotito_molona.jpg')
                cv2.imwrite(save_path, colors[max_color][1])
                self.get_logger().info(f'Saved image to {save_path}')
                self.image_saved = True
                self.image_sub.destroy()
            except Exception as e:
                self.get_logger().error(f'Error processing image: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    image_saver = ImageSaver()
    test_image_path = '/home/cmarrod3/Desktop/fotito_molona.jpg'
    try:
        while rclpy.ok():
            rclpy.spin_once(image_saver, timeout_sec=0.1)
            prediction = load_and_predict(test_image_path)

            if prediction < 0.5:
                print("Es una imagen de camiseta.")
            else:
                print("Es una imagen de jeans.")
    except KeyboardInterrupt:
        image_saver.get_logger().info('Shutting down')
    finally:
        image_saver.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

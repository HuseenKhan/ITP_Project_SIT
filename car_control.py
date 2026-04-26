import threading
import tkinter as tk

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


# This class creates a ROS2 node for controlling the Yahboom car
class YahboomTeleopGUI(Node):
    def __init__(self):
        # Initialize the ROS2 node with the name 'yahboom_teleop_gui'
        super().__init__('yahboom_teleop_gui')

        # Create a publisher that sends Twist velocity commands to /cmd_vel
        # The Yahboom car usually receives movement commands from this topic
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)



        # angular controls left/right rotation
        self.current_linear = 0.0
        # angular controls left/right rotation
        self.current_angular = 0.0

        # Default speed values
        self.linear_speed = 0.25
        self.angular_speed = 0.8

        # Create a timer that calls publish_current_cmd every 0.05 seconds
        # This keeps publishing the command while a key or button is held
        self.timer = self.create_timer(0.05, self.publish_current_cmd)

        # Print a message in the ROS terminal
        self.get_logger().info('Yahboom teleop GUI started')

    def publish_current_cmd(self):
        # Create a Twist message
        msg = Twist()

        # Set forward/backward speed
        msg.linear.x = self.current_linear

        # Set left/right turning speed
        msg.angular.z = self.current_angular

        # Publish the velocity command to the robot
        self.cmd_pub.publish(msg)

    def set_motion(self, linear_x=0.0, angular_z=0.0):
        # Update the current movement command
        self.current_linear = linear_x
        self.current_angular = angular_z

    def stop_motion(self):
        # Set both linear and angular speeds to zero
        self.current_linear = 0.0
        self.current_angular = 0.0

        # Publish a stop command immediately
        msg = Twist()
        self.cmd_pub.publish(msg)


def main():
    # Initialize ROS2
    rclpy.init()

    # Create the Yahboom teleoperation node
    node = YahboomTeleopGUI()

    # Run ROS2 spinning in a separate thread
    # This allows ROS2 to keep working while Tkinter GUI is running
    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Yahboom Car Control")
    root.geometry("320x320")
    root.resizable(False, False)

    # Add instruction text to the GUI
    info = tk.Label(
        root,
        text="Hold button or keyboard key\nW=Forward  S=Backward  A=Left  D=Right",
        font=("Arial", 11)
    )
    info.pack(pady=10)

    # Create a frame to hold the buttons
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # -------- Button press/release handlers --------

    # Move the robot forward
    def press_forward(event=None):
        node.set_motion(linear_x=node.linear_speed, angular_z=0.0)

    # Move the robot backward
    def press_backward(event=None):
        node.set_motion(linear_x=-node.linear_speed, angular_z=0.0)

    # Turn the robot left
    def press_left(event=None):
        node.set_motion(linear_x=0.0, angular_z=node.angular_speed)

    # Turn the robot right
    def press_right(event=None):
        node.set_motion(linear_x=0.0, angular_z=-node.angular_speed)

    # Stop the robot when button/key is released
    def release_stop(event=None):
        node.stop_motion()

    # -------- Graphical User Interface ---------

    # Create movement buttons
    btn_forward = tk.Button(frame, text="Forward", width=12, height=2)
    btn_backward = tk.Button(frame, text="Backward", width=12, height=2)
    btn_left = tk.Button(frame, text="Left", width=12, height=2)
    btn_right = tk.Button(frame, text="Right", width=12, height=2)

    # Create STOP button
    # This button directly calls node.stop_motion when clicked
    btn_stop = tk.Button(
        frame,
        text="STOP",
        width=12,
        height=2,
        bg="red",
        fg="white",
        command=node.stop_motion
    )

    # Arrange buttons in a simple control layout
    btn_forward.grid(row=0, column=1, padx=5, pady=5)
    btn_left.grid(row=1, column=0, padx=5, pady=5)
    btn_stop.grid(row=1, column=1, padx=5, pady=5)
    btn_right.grid(row=1, column=2, padx=5, pady=5)
    btn_backward.grid(row=2, column=1, padx=5, pady=5)

    # Press and hold behavior for buttons
    # When mouse button is pressed, robot starts moving
    # When mouse button is released, robot stops
    btn_forward.bind("<ButtonPress-1>", press_forward)
    btn_forward.bind("<ButtonRelease-1>", release_stop)

    btn_backward.bind("<ButtonPress-1>", press_backward)
    btn_backward.bind("<ButtonRelease-1>", release_stop)

    btn_left.bind("<ButtonPress-1>", press_left)
    btn_left.bind("<ButtonRelease-1>", release_stop)

    btn_right.bind("<ButtonPress-1>", press_right)
    btn_right.bind("<ButtonRelease-1>", release_stop)

    # Instead of using the mouse, we can also use the keyboard

    # This function runs when a keyboard key is pressed
    def on_key_press(event):
        # Convert key name to lowercase
        key = event.keysym.lower()

        # Check which key is pressed and move accordingly
        if key == 'w':
            press_forward()
        elif key == 's':
            press_backward()
        elif key == 'a':
            press_left()
        elif key == 'd':
            press_right()

    # This function runs when a keyboard key is released
    def on_key_release(event):
        key = event.keysym.lower()

        # Stop the robot when movement keys are released
        if key in ['w', 'a', 's', 'd']:
            release_stop()

    # Connect keyboard press and release events to the functions
    root.bind("<KeyPress>", on_key_press)
    root.bind("<KeyRelease>", on_key_release)

    # Give keyboard focus to the window
    # This helps keyboard events work immediately
    root.focus_force()

    # This function runs when the GUI window is closed
    def on_close():
        # Stop the robot before closing
        node.stop_motion()

        # Destroy the ROS2 node
        node.destroy_node()

        # Shutdown ROS2
        rclpy.shutdown()

        # Close the Tkinter window
        root.destroy()

    # Call on_close when the user closes the window
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Start the Tkinter GUI loop
    root.mainloop()


# Run the main function when this file is executed directly
if __name__ == '__main__':
    main()
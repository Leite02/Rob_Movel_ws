#!/usr/bin/env python3

import math

import rospy
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion


class WaypointRecorder:

    def __init__(self):

        self.waypoint_atual = None
        self.aguardando_clique = False

        rospy.Subscriber(
            "/move_base_simple/goal",
            PoseStamped,
            self.callback
        )

    def callback(self, msg):

        if not self.aguardando_clique:
            return

        x = msg.pose.position.x
        y = msg.pose.position.y

        q = msg.pose.orientation

        quaternion = (
            q.x,
            q.y,
            q.z,
            q.w
        )

        (_, _, yaw) = euler_from_quaternion(quaternion)

        yaw_deg = math.degrees(yaw)

        print("\n===================================")
        print("Waypoint {} registrado!".format(self.waypoint_atual))
        print("X    : {:.3f}".format(x))
        print("Y    : {:.3f}".format(y))
        print("Yaw  : {:.1f}°".format(yaw_deg))
        print("===================================\n")

        self.aguardando_clique = False

    def executar(self):

        while not rospy.is_shutdown():

            try:

                numero = input("Digite o waypoint (1-16) ou 0 para sair: ")

                numero = int(numero)

                if numero == 0:
                    print("Encerrando...")
                    break

                if numero < 1 or numero > 16:
                    print("Waypoint inválido.\n")
                    continue

                self.waypoint_atual = numero
                self.aguardando_clique = True

                print("\nClique no mapa usando o 2D Nav Goal.\n")

                while self.aguardando_clique and not rospy.is_shutdown():
                    rospy.sleep(0.1)

            except ValueError:
                print("Digite apenas números.\n")


if __name__ == "__main__":

    rospy.init_node("gravar_waypoints")

    recorder = WaypointRecorder()

    print("\n===================================")
    print("     GRAVADOR DE WAYPOINTS")
    print("===================================\n")

    recorder.executar()

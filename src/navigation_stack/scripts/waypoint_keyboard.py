#!/usr/bin/env python3

import rospy
import yaml
import os
import actionlib

from geometry_msgs.msg import Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler


class WaypointNavigator:

    def __init__(self):

        rospy.init_node("waypoint_keyboard")

        self.waypoints = self.carregar_waypoints()

        self.client = actionlib.SimpleActionClient(
            "/move_base",
            MoveBaseAction
        )

        rospy.loginfo("Esperando move_base...")

        self.client.wait_for_server()

        rospy.loginfo("move_base conectado!")


    def carregar_waypoints(self):

        caminho = os.path.expanduser(
            "~/Rob_Movel_ws/src/navigation_stack/config/waypoints.yaml"
        )

        with open(caminho, "r") as arquivo:
            dados = yaml.safe_load(arquivo)

        return dados["waypoints"]


    def enviar_waypoint(self, numero):

        ponto = self.waypoints[numero]

        x = ponto["x"]
        y = ponto["y"]
        yaw = ponto["yaw"]


        quat = quaternion_from_euler(
            0,
            0,
            yaw
        )


        goal = MoveBaseGoal()

        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y

        goal.target_pose.pose.orientation = Quaternion(
            quat[0],
            quat[1],
            quat[2],
            quat[3]
        )


        rospy.loginfo(
            "Enviando waypoint %d",
            numero
        )


        self.client.send_goal(goal)


        while not rospy.is_shutdown():

            terminou = self.client.wait_for_result(
                rospy.Duration(0.5)
            )


            if terminou:

                estado = self.client.get_state()


                # SUCCEEDED
                if estado == 3:

                    rospy.loginfo(
                        "Waypoint %d alcançado!",
                        numero
                    )

                    return True


                else:

                    rospy.logwarn(
                        "Falha no waypoint %d",
                        numero
                    )

                    return False



    def executar_rota(self, rota):

        print("\n==============================")
        print(" EXECUTANDO ROTA")
        print("==============================")


        for ponto in rota:

            print("\nIndo para waypoint", ponto)


            sucesso = self.enviar_waypoint(ponto)


            if not sucesso:

                print("\nRota interrompida!")

                return


        print("\n==============================")
        print(" ROTA FINALIZADA")
        print("==============================")



    def executar(self):

        while not rospy.is_shutdown():

            print("\n==============================")
            print(" NAVEGAÇÃO POR WAYPOINTS")
            print("==============================")
            print("Exemplo:")
            print("  5")
            print("  rota 1 5 9 13")
            print("0 - sair")


            entrada = input("\nDestino: ")



            if entrada == "0":

                print("Encerrando...")
                break



            if entrada.startswith("rota"):

                try:

                    valores = entrada.split()

                    rota = [
                        int(x)
                        for x in valores[1:]
                    ]


                    self.executar_rota(rota)


                except:

                    print("Formato inválido")

                continue



            try:

                numero = int(entrada)


                if numero not in self.waypoints:

                    print("Waypoint inválido")
                    continue


                self.enviar_waypoint(numero)



            except ValueError:

                print("Digite um número válido")



if __name__ == "__main__":

    try:

        nav = WaypointNavigator()

        nav.executar()


    except rospy.ROSInterruptException:

        pass

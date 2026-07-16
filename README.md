# Rob_Movel_ws

## Simulação de Robô Móvel Autônomo em ROS Noetic

Este repositório contém o workspace ROS utilizado para simulação, mapeamento e navegação autônoma de um robô móvel utilizando **ROS Noetic**, **Gazebo 11** e **RViz**.

O projeto foi desenvolvido com foco em uma aplicação de robótica móvel em ambiente interno, utilizando um robô diferencial equipado com sensor **LiDAR** para criação de mapas e posterior navegação autônoma.

<img width="1468" height="1080" alt="VID-20260716-WA0003(2)" src="https://github.com/user-attachments/assets/b92e6d49-1ecf-4dd9-a6a8-bbbb7c13ace2" />


---

# Funcionalidades

O projeto permite:

- Simulação do robô móvel no Gazebo
- Criação de mapas utilizando SLAM (GMapping)
- Visualização do ambiente no RViz
- Localização do robô utilizando AMCL
- Navegação autônoma utilizando Move Base
- Planejamento de trajetória em ambiente conhecido
- Controle manual via teleoperação
- Testes em ambiente de armazém simulado
- Navegação utilizando pontos fixos (waypoints)
- Execução de rotas sequenciais entre diferentes pontos do mapa
- Controle de destinos pelo terminal utilizando comandos de teclado

---

# Ambiente de Desenvolvimento

## Software utilizado

- Ubuntu 20.04
- ROS Noetic
- Gazebo 11
- RViz
- Catkin Workspace

---

# Principais Pacotes ROS

- `gazebo_ros`
- `slam_gmapping`
- `map_server`
- `amcl`
- `move_base`
- `rviz`
- `navigation stack`

---

# Estrutura do Workspace

```
Rob_Movel_ws
│
├── src
│   │
│   ├── atom
│   │   ├── launch
│   │   ├── urdf
│   │   ├── meshes
│   │   ├── model
│   │   ├── worlds
│   │   └── scripts
│   │
│   ├── navigation_stack
│   │   ├── launch
│   │   ├── param
│   │   ├── rviz
│   │   ├── config
│   │   │   └── waypoints.yaml
│   │   ├── scripts
│   │   │   └── waypoint_keyboard.py
│   │   └── src
│   │
│   └── maps
│       └── armazem_leve
│           ├── map.yaml
│           └── map.pgm
│
└── README.md
```

---

# Instalação

## 1. Criar workspace

```bash
mkdir -p ~/Rob_Movel_ws/src

cd ~/Rob_Movel_ws
```

---

## 2. Clonar o repositório

```bash
git clone https://github.com/Leite02/Rob_Movel_ws.git
```

---

## 3. Instalar dependências ROS

```bash
sudo apt update

sudo apt install \
ros-noetic-gazebo-ros \
ros-noetic-gmapping \
ros-noetic-navigation \
ros-noetic-map-server \
ros-noetic-amcl \
ros-noetic-move-base
```

---

## 4. Compilar o workspace

Dentro do workspace:

```bash
cd ~/Rob_Movel_ws

catkin_make
```

Após a compilação:

```bash
source devel/setup.bash
```

---

# Execução

# 1. Mapeamento do ambiente (SLAM)

Para criar um novo mapa:

```bash
roslaunch atom atom_mapping.launch
```

Esse comando inicia:

- Gazebo
- Robô móvel
- Sensor LiDAR
- GMapping
- RViz configurado para mapeamento

Durante o mapeamento, mova o robô utilizando teleoperação.

Após finalizar, salve o mapa:

```bash
rosrun map_server map_saver -f ~/Rob_Movel_ws/src/maps/nome_do_mapa
```

Serão gerados:

```
nome_do_mapa.yaml
nome_do_mapa.pgm
```

---

# Navegação Autônoma

Com o mapa previamente criado:

```bash
roslaunch atom armazem_navigation.launch
```

Esse launch inicia:

- Gazebo com ambiente conhecido
- Map Server
- AMCL para localização
- Move Base
- RViz para navegação

No RViz:

Inicialize a posição do robô utilizando:

```
2D Pose Estimate
```

Defina o destino utilizando:

```
2D Nav Goal
```

O robô irá calcular uma trajetória e navegar automaticamente.

---

# Navegação utilizando Waypoints

Além da navegação pelo RViz, o projeto possui um sistema de navegação utilizando pontos previamente definidos no mapa.

Os pontos são armazenados no arquivo:

```
~/Rob_Movel_ws/src/navigation_stack/config/waypoints.yaml
```

Cada waypoint possui:

- posição X
- posição Y
- orientação do robô (Yaw)

Exemplo:

```yaml
waypoints:
  1:
    x: 7.323
    y: 6.041
    yaw: -3.14
```

---

# Executando navegação por Waypoints

Primeiro inicie a navegação:

```bash
roslaunch atom armazem_navigation.launch
```

Em outro terminal:

```bash
source ~/Rob_Movel_ws/devel/setup.bash

rosrun navigation_stack waypoint_keyboard.py
```

O programa exibirá:

```
NAVEGAÇÃO POR WAYPOINTS
```

Digite o número do waypoint desejado.

Exemplo:

```
5
```

O robô irá navegar automaticamente até o ponto 5.

---

# Execução de Rotas

Também é possível executar uma sequência de pontos.

Exemplo:

```
rota 1 5 9 13
```

O robô executará:

```
Waypoint 1
      ↓
Waypoint 5
      ↓
Waypoint 9
      ↓
Waypoint 13
```

Ao finalizar:

```
ROTA FINALIZADA
```

<img width="860" height="583" alt="VID-20260716-WA0003(1)" src="https://github.com/user-attachments/assets/3f04dda6-2bf2-4ffe-8f47-6c68d1e6fa26" />


---

# Alteração dos Waypoints

Para criar ou modificar pontos de navegação:

Editar:

```
~/Rob_Movel_ws/src/navigation_stack/config/waypoints.yaml
```

Os pontos devem estar dentro da região conhecida pelo mapa utilizado pelo AMCL.

---

# Controle Manual

O robô pode ser movimentado utilizando comandos de velocidade:

```bash
rostopic pub /atom/cmd_vel geometry_msgs/Twist \
'{linear: {x: 0.2, y: 0.0, z: 0.0},
angular: {x: 0.0, y: 0.0, z: 0.0}}'
```

---

# Principais Launch Files

## Mapeamento

```
atom/launch/atom_mapping.launch
```

Executa o processo de SLAM.

---

## Navegação

```
atom/launch/armazem_navigation.launch
```

Executa navegação autônoma utilizando mapa existente.

---

## Mundo Gazebo

```
atom/launch/atom_warehouse.launch
```

Carrega o ambiente simulado.

---

# Sensores

O robô possui:

## LiDAR

Responsável por:

- criação do mapa
- localização
- detecção de obstáculos

Tópico:

```
/scan
```

---

## Odometria

Responsável pela estimativa de movimento:

```
/atom/odom
```

---

## Controle de velocidade

Comando:

```
/atom/cmd_vel
```

---

# Mapa utilizado

O projeto utiliza o ambiente:

```
maps/armazem_leve
```

Contendo:

```
map.yaml
map.pgm
```

O mapa foi criado utilizando GMapping através do sensor LiDAR do robô.

---

# Solução de Problemas

## Robô aparece no lugar errado no RViz

Utilize:

```
2D Pose Estimate
```

e informe a posição inicial.

---

## Não aparecem tópicos ROS

Verifique se o ambiente foi carregado:

```bash
source ~/Rob_Movel_ws/devel/setup.bash
```

---

## Gazebo abre mas robô não se move

Verifique:

```bash
rostopic list | grep cmd_vel
```

Deve existir:

```
/atom/cmd_vel
```

---

## Waypoint não inicia

Verifique se o arquivo existe:

```bash
ls ~/Rob_Movel_ws/src/navigation_stack/config/
```

Deve aparecer:

```
waypoints.yaml
```

Verifique a permissão do script:

```bash
chmod +x ~/Rob_Movel_ws/src/navigation_stack/scripts/waypoint_keyboard.py
```

---

# Licença

Este projeto está disponibilizado para fins acadêmicos e de pesquisa.

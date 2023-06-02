import numpy as np
from frmovewrapper.frmove import FRCobot
import frmovewrapper.robotmath as rm
import copy
import time


class FRPalletize(object):
    """
        A Palletization template

        Author: wangyan
        Date: 2023/06/02
    """

    def __init__(self, params) -> None:

        self.rbt = FRCobot()
        # 读取参数配置
        self.params = params


    def euler_to_homomat(self, euler):
        for i in range(3,6):
            euler[i] = np.deg2rad(euler[i])
        rotmat = rm.rotmat_from_euler(euler[3], euler[4], euler[5])
        return rm.homomat_from_posrot(np.asarray(euler[:3]), rotmat)


    def euler_from_homomat(self, homomat):
        rpy = rm.rotmat_to_euler(homomat[:3, :3])
        euler = np.concatenate((homomat[:3, 3], rpy))
        for i in range(3,6):
            euler[i] = np.rad2deg(euler[i])
        for i in range(6):
            euler = list(euler)
            euler[i] = float(euler[i])
        return euler
        

    def get_target_point(self, box_point, first_corner, move_direction, 
                         p_path, p_pathz, p_pallet_origin, p_suction_point, 
                         appr_offset=[50,50,50]):
        """
            获得机器人坐标系下的机器人运动目标点

            参数:
                box_point: 托盘坐标系下工件的位置[x, y, z]
                first_corner: 机器人运动起始方位
                move_direction: 机器人移动方向
                p_path: 机器人坐标系下,示教得到的平面路径点,用于确定托盘坐标系的X或Y轴
                p_pathz: 机器人坐标系下,示教得到的法向路径点,用于确定托盘坐标系的Z轴
                p_pallet_origin: 机器人坐标系下,示教得到的托盘坐标系原点坐标
                p_suction_point: 机器人坐标系下,示教得到的吸盘在工件上的吸附位置,通常和工件几何中心重合
                appr_offset: 目标渐近点偏移量,使机器人从无遮挡物的方向向目标靠近

            返回:
                target_point: 机器人坐标系下,机器人的运动目标点
        """

        (x, y, z) = box_point
        tran_tcp_ppo_to_robot = self.euler_to_homomat(p_pallet_origin)  # ppo=p_pallet_origin
        tran_tcp_psp_to_robot = self.euler_to_homomat(p_suction_point) # psp=p_suction_point
        tran_tcp_path_to_robot = self.euler_to_homomat(p_path)
        tran_tcp_pathz_to_robot = self.euler_to_homomat(p_pathz)
        
        # 根据路径点确定托盘坐标系
        z_pallet_to_robot = tran_tcp_pathz_to_robot[:3,3] - tran_tcp_path_to_robot[:3,3]
        if move_direction == 'X':
            if first_corner[0] == 0:
                x_pallet_to_robot = tran_tcp_path_to_robot[:3,3] - tran_tcp_ppo_to_robot[:3,3]
            elif first_corner[0] == 1:
                x_pallet_to_robot = -(tran_tcp_path_to_robot[:3,3] - tran_tcp_ppo_to_robot[:3,3])
            else:
                raise ValueError("[参数错误]无效的起始方位,必须是[0,0]、[0,1]、[1,0]或[1,1]")
            y_pallet_to_robot = np.cross(z_pallet_to_robot, x_pallet_to_robot)
        elif move_direction == 'Y':
            if first_corner[1] == 0:
                y_pallet_to_robot = tran_tcp_path_to_robot[:3,3] - tran_tcp_ppo_to_robot[:3,3]
            elif first_corner[1] == 1:
                y_pallet_to_robot = -(tran_tcp_path_to_robot[:3,3] - tran_tcp_ppo_to_robot[:3,3])
            else:
                raise ValueError("[参数错误]无效的起始方位,必须是[0,0]、[0,1]、[1,0]或[1,1]")
            x_pallet_to_robot = np.cross(y_pallet_to_robot, z_pallet_to_robot)
        else:
            raise ValueError("[参数错误]无效的移动方向,必须是'X'或'Y'")
        
        tran_pallet_to_robot_rotmat = np.vstack([rm.unit_vector(x_pallet_to_robot), 
                                                rm.unit_vector(y_pallet_to_robot), 
                                                rm.unit_vector(z_pallet_to_robot)]).T
        tran_pallet_to_robot = rm.homomat_from_posrot(pos=tran_tcp_ppo_to_robot[:3,3], 
                                                      rot=tran_pallet_to_robot_rotmat)
        
        # 进行必要的坐标变换
        tran_pallet_to_tcp = rm.homomat_from_posrot(pos=np.zeros(3),
                                rot=np.linalg.inv(tran_tcp_ppo_to_robot[:3,:3]) @ tran_pallet_to_robot_rotmat)
        tran_suction_to_tcp = tran_pallet_to_tcp
        tran_suction_to_robot = tran_tcp_psp_to_robot @ tran_suction_to_tcp
        tran_suction_to_box = rm.homomat_from_posrot(
            pos=np.linalg.inv(tran_pallet_to_robot[:3,:3]) @ (tran_suction_to_robot[:3,3]-tran_pallet_to_robot[:3,3]),
            rot=np.linalg.inv(tran_pallet_to_robot[:3,:3]) @ tran_suction_to_robot[:3,:3])

        # 目标点计算
        tran_box_to_pallet = self.euler_to_homomat([x, y, z, 0., 0., 0.])
        tran_suctionbox_to_robot = tran_pallet_to_robot @ (tran_box_to_pallet @ tran_suction_to_box)
        tran_tcp_target_to_robot = tran_suctionbox_to_robot @ rm.homomat_inverse(tran_suction_to_tcp)
        target_point = self.euler_from_homomat(tran_tcp_target_to_robot)

        # 目标渐近点计算
        appr_offset_x = appr_offset[0] if first_corner[0] == 0 else -appr_offset[0]
        appr_offset_y = appr_offset[1] if first_corner[1] == 0 else -appr_offset[1]
        tran_boxappr_to_pallet = self.euler_to_homomat([x+appr_offset_x, y+appr_offset_y, z+appr_offset[2], 0., 0., 0.])
        tran_suctionappr_to_robot = tran_pallet_to_robot @ (tran_boxappr_to_pallet @ tran_suction_to_box)
        tran_tcp_targetappr_to_robot = tran_suctionappr_to_robot @ rm.homomat_inverse(tran_suction_to_tcp)
        target_appr_point = self.euler_from_homomat(tran_tcp_targetappr_to_robot)

        return target_point, target_appr_point


    def robot_motion(self, robot, point, motion_type, vel=50.0):
        """
            机器人的两种运动方式: 1.点到点(MoveJ) 2.直线(MoveL)
        """
        if motion_type == 'ptp':
            robot.MoveJ(point, target_flag='desc',vel=vel)
        elif motion_type == 'line':
            robot.MoveL(point, target_flag='desc',vel=vel)
        else:
            raise ValueError("[参数错误]无效的运动方式,必须是'ptp'或'line'")


    def execute_palletize(self, suction=True):
        """
            执行码垛任务
        """
        # 工件参数
        box_length = self.params['工件配置']['工件长度']
        box_width = self.params['工件配置']['工件宽度']
        box_height = self.params['工件配置']['工件高度']
        p_suction_point = self.params['工件配置']['吸盘位置']

        # 托盘参数
        pallet_length = self.params['托盘配置']['前边长度']
        pallet_width = self.params['托盘配置']['侧边长度']

        # 模式参数
        box_interval = self.params['模式配置']['工件间隔']
        nrow = self.params['模式配置']['每层行数']
        ncol = self.params['模式配置']['每层列数']
        nlayer = self.params['模式配置']['码垛层数']

        # 机械臂移动参数
        p_home = self.params['机器人移动配置']['作业原点']
        p_prepare = self.params['机器人移动配置']['作业准备点']
        p_mid = self.params['机器人移动配置']['工位过渡点']
        p_pallet_origin = self.params['机器人移动配置']['托盘原点']
        p_path = self.params['机器人移动配置']['平面路径点']
        p_pathz = self.params['机器人移动配置']['法向路径点']
        first_corner = self.params['机器人移动配置']['起始方位']
        move_direction = self.params['机器人移动配置']['移动方向']
        motion = self.params['机器人移动配置']['运动方式']
        pattern = self.params['机器人移动配置']['运动路径']
        work_direction = self.params['机器人移动配置']['堆叠方式']
        
        # 数据预检查
        if (nrow*(box_width+box_interval)-box_interval > pallet_width):
            raise ValueError("[Warning] 工件超出托盘侧边范围!")
        if (ncol*(box_length+box_interval)-box_interval > pallet_length):
            raise ValueError("[Warning] 工件超出托盘前边范围!")

        # 计算工件在托盘上的访问位置和顺序
        box_points = []
        start_layer, end_layer, step_layer = 0, nlayer, 1

        for layer in range(start_layer, end_layer, step_layer):
            # 计算当前层高度
            z = layer * box_height
            # 16 situations: 4 corners x 2 move_directions x 2 patterns
            # 选择起始方位,方位代表的位置如下图所示: [0,0] / [0,1] / [1,0] / [1,1]
            # ================== Y
            # |[0,0]      [0,1]|
            # |                |
            # |                |
            # |                |
            # |[1,0]      [1,1]|
            # ==================
            # X
            if first_corner == [0,0]:
                # 选择运动方向: 'Y'--沿托盘前边 / ‘X’--沿托盘侧边
                if move_direction == 'Y':
                    for row in range(nrow):
                        x = row * (box_width + box_interval)
                        # 选择每层的运动路径: 头到尾--headtail / 弓字形--zigzag
                        if pattern == 'headtail':
                            start_col, end_col, step_col = 0, ncol, 1
                        elif pattern == 'zigzag':
                            # 根据行号和顺序变量确定每行的起始点和方向
                            if row % 2 == 0:
                                start_col, end_col, step_col = 0, ncol, 1
                            else:
                                start_col, end_col, step_col = ncol-1, -1, -1
                        else:
                            raise ValueError("[参数错误]无效的运动路径,必须是'headtail'或'zigzag'")
                        for col in range(start_col, end_col, step_col):
                            y = col * (box_length + box_interval)
                            box_points.append((x,y,z))
                elif move_direction == 'X':
                    for col in range(ncol):
                        y = col * (box_length + box_interval)
                        if pattern == 'headtail':
                            start_row, end_row, step_row = 0, nrow, 1
                        elif pattern == 'zigzag':
                            if col % 2 == 0:
                                start_row, end_row, step_row = 0, nrow, 1
                            else:
                                start_row, end_row, step_row = nrow-1, -1, -1
                        else:
                            raise ValueError("[参数错误]无效的运动路径,必须是'headtail'或'zigzag'")
                        for row in range(start_row, end_row, step_row):
                            x = row * (box_width + box_interval)
                            box_points.append((x,y,z))
                else:
                    raise ValueError("[参数错误]无效的移动方向,必须是'X'或'Y'")

            elif first_corner == [0,1]:
                if move_direction == 'Y':
                    for row in range(nrow):
                        x = row * (box_width + box_interval)
                        if pattern == 'headtail':
                            start_col, end_col, step_col = 0, -ncol, -1
                        elif pattern == 'zigzag':
                            if row % 2 == 0:
                                start_col, end_col, step_col = 0, -ncol, -1
                            else:
                                start_col, end_col, step_col = -ncol+1, 1, 1
                        else:
                            raise ValueError("[参数错误]无效的运动路径,必须是'headtail'或'zigzag'")
                        for col in range(start_col, end_col, step_col):
                            y = col * (box_length + box_interval)
                            box_points.append((x,y,z))
                elif move_direction == 'X':
                    for col in range(0,-ncol,-1):
                        y = col * (box_length + box_interval)
                        if pattern == 'headtail':
                            start_row, end_row, step_row = 0, nrow, 1
                        elif pattern == 'zigzag':
                            if col % 2 == 0:
                                start_row, end_row, step_row = 0, nrow, 1
                            else:
                                start_row, end_row, step_row = nrow-1, -1, -1
                        else:
                            raise ValueError("[参数错误]无效的运动路径,必须是'headtail'或'zigzag'")
                        for row in range(start_row, end_row, step_row):
                            x = row * (box_width + box_interval)
                            box_points.append((x,y,z))
                else:
                    raise ValueError("[参数错误]无效的移动方向,必须是'X'或'Y'")

            elif first_corner == [1,0]:
                if move_direction == 'Y':
                    for row in range(0,-nrow,-1):
                        x = row * (box_width + box_interval)
                        if pattern == 'headtail':
                            start_col, end_col, step_col = 0, ncol, 1
                        elif pattern == 'zigzag':
                            if row % 2 == 0:
                                start_col, end_col, step_col = 0, ncol, 1
                            else:
                                start_col, end_col, step_col = ncol-1, -1, -1
                        else:
                            raise ValueError("[参数错误]无效的运动路径,必须是'headtail'或'zigzag'")
                        for col in range(start_col, end_col, step_col):
                            y = col * (box_length + box_interval)
                            box_points.append((x,y,z))
                elif move_direction == 'X':
                    for col in range(ncol):
                        y = col * (box_length + box_interval)
                        if pattern == 'headtail':
                            start_row, end_row, step_row = 0, -nrow, -1
                        elif pattern == 'zigzag':
                            if col % 2 == 0:
                                start_row, end_row, step_row = 0, -nrow, -1
                            else:
                                start_row, end_row, step_row = -nrow+1, 1, 1
                        else:
                            raise ValueError("[参数错误]无效的运动路径,必须是'headtail'或'zigzag'")
                        for row in range(start_row, end_row, step_row):
                            x = row * (box_width + box_interval)
                            box_points.append((x,y,z))
                else:
                    raise ValueError("[参数错误]无效的移动方向,必须是'X'或'Y'")

            elif first_corner == [1,1]:
                if move_direction == 'Y':
                    for row in range(0,-nrow,-1):
                        x = row * (box_width + box_interval)
                        if pattern == 'headtail':
                            start_col, end_col, step_col = 0, -ncol, -1
                        elif pattern == 'zigzag':
                            if row % 2 == 0:
                                start_col, end_col, step_col = 0, -ncol, -1
                            else:
                                start_col, end_col, step_col = -ncol+1, 1, 1
                        else:
                            raise ValueError("[参数错误]无效的运动路径,必须是'headtail'或'zigzag'")
                        for col in range(start_col, end_col, step_col):
                            y = col * (box_length + box_interval)
                            box_points.append((x,y,z))
                elif move_direction == 'X':
                    for col in range(0,-ncol,-1):
                        y = col * (box_length + box_interval)
                        if pattern == 'headtail':
                            start_row, end_row, step_row = 0, -nrow, -1
                        elif pattern == 'zigzag':
                            if col % 2 == 0:
                                start_row, end_row, step_row = 0, -nrow, -1
                            else:
                                start_row, end_row, step_row = -nrow+1, 1, 1
                        else:
                            raise ValueError("[参数错误]无效的运动路径,必须是'headtail'或'zigzag'")
                        for row in range(start_row, end_row, step_row):
                            x = row * (box_width + box_interval)
                            box_points.append((x,y,z))
                else:
                    raise ValueError("[参数错误]无效的移动方向,必须是'X'或'Y'")
            
            else:
                raise ValueError("[参数错误]无效的起始方位,必须是[0,0]、[0,1]、[1,0]或[1,1]")
        
        # 选择堆叠方式: 码垛--load / 卸垛--unload
        if work_direction == 'load':
            # 计算机器人坐标系下的目标点坐标
            for index, box_point in enumerate(box_points):
                pallet_origin = copy.deepcopy(p_pallet_origin)
                suction_point = copy.deepcopy(p_suction_point)
                mid_point = copy.deepcopy(p_mid)
                path_point = copy.deepcopy(p_path)
                path_pointz = copy.deepcopy(p_pathz)
                index_layer = index//(nrow*ncol)
                index_box = index%(nrow*ncol)
                mid_point[2] += index_layer*box_height
                target_point, target_appr_point = self.get_target_point(
                                                    box_point, 
                                                    first_corner, 
                                                    move_direction,
                                                    p_path=path_point,
                                                    p_pathz=path_pointz,
                                                    p_pallet_origin=pallet_origin, 
                                                    p_suction_point=suction_point) 
                print(f"[运行状态]托盘坐标系下第{index_layer+1}/{nlayer}层,第{index_box+1}/{nrow*ncol}个工件位置: {box_point}")
                print(f"[运行状态]机器人坐标系下目标点: {target_point}")
                
                # 机械臂移动到作业准备点
                self.robot_motion(self.rbt, p_prepare, motion_type=motion, vel=100.0)
                # 机械臂移动到作业原点
                self.robot_motion(self.rbt, p_home, motion_type=motion)
                # 拿起工件
                if suction:
                    time.sleep(1.0)
                    self.rbt.robot.SetDO(4,1,0,0)  # 吸盘吸取
                    time.sleep(2.0)
                # 机械臂移动到作业准备点
                self.robot_motion(self.rbt, p_prepare, motion_type=motion, vel=100.0)
                # 机械臂移动到工位过渡点
                self.robot_motion(self.rbt, mid_point, motion_type=motion, vel=100.0)
                # 移动机器人到目标渐近点
                self.robot_motion(self.rbt, target_appr_point, motion_type=motion, vel=100.0)
                # 移动机器人到目标点
                self.robot_motion(self.rbt, target_point, motion_type=motion, vel=10.0)
                # 释放工件
                if suction:
                    time.sleep(1.0)
                    self.rbt.robot.SetDO(4,0,0,0)  # 吸盘释放
                    time.sleep(2.0)
                # 移动机器人到目标渐近点
                self.robot_motion(self.rbt, target_appr_point, motion_type=motion, vel=10.0)
                # 机械臂移动到工位过渡点
                self.robot_motion(self.rbt, mid_point, motion_type=motion, vel=100.0)
                # 机械臂移动到作业准备点
                self.robot_motion(self.rbt, p_prepare, motion_type=motion, vel=100.0)
        
        elif work_direction == 'unload':
            # 计算机器人坐标系下的目标点坐标
            for index, box_point in enumerate(box_points[::-1]):
                pallet_origin = copy.deepcopy(p_pallet_origin)
                suction_point = copy.deepcopy(p_suction_point)
                mid_point = copy.deepcopy(p_mid)
                path_point = copy.deepcopy(p_path)
                path_pointz = copy.deepcopy(p_pathz)
                home_point = copy.deepcopy(p_home)
                index_layer = (nlayer - 1 - index//(nrow*ncol))
                index_box = index%(nrow*ncol)
                mid_point[2] += index_layer*box_height
                target_point, target_appr_point = self.get_target_point(
                                                    box_point, 
                                                    first_corner, 
                                                    move_direction,
                                                    p_path=path_point,
                                                    p_pathz=path_pointz,
                                                    p_pallet_origin=pallet_origin, 
                                                    p_suction_point=suction_point) 
                print(f"[运行状态]托盘坐标系下{index_layer+1}/{nlayer}层,第{index_box+1}/{nrow*ncol}个工件位置: {box_point}")
                print(f"[运行状态]机器人坐标系下目标点: {target_point}")
                
                # 机械臂移动到作业准备点
                self.robot_motion(self.rbt, p_prepare, motion_type=motion, vel=100.0)
                # 机械臂移动到工位过渡点
                self.robot_motion(self.rbt, mid_point, motion_type=motion, vel=100.0)
                # 移动机器人到目标渐近点 
                self.robot_motion(self.rbt, target_appr_point, motion_type=motion, vel=100.0)
                # 移动机器人到目标点
                target_point[2] -= 30 
                self.robot_motion(self.rbt, target_point, motion_type=motion, vel=10.0)
                # 拿起工件
                if suction:
                    time.sleep(1.0)
                    self.rbt.robot.SetDO(4,1,0,0)  # 吸盘吸取
                    time.sleep(2.0)
                # 移动机器人到目标渐近点
                self.robot_motion(self.rbt, target_appr_point, motion_type=motion, vel=10.0)
                # 机械臂移动到工位过渡点
                self.robot_motion(self.rbt, mid_point, motion_type=motion, vel=100.0)
                # 机械臂移动到作业准备点
                self.robot_motion(self.rbt, p_prepare, motion_type=motion, vel=100.0)
                # 机械臂移动到作业原点
                home_point[2] += 20
                self.robot_motion(self.rbt, home_point, motion_type=motion, vel=100.0)
                # 释放工件
                if suction:
                    time.sleep(1.0)
                    self.rbt.robot.SetDO(4,0,0,0)  # 吸盘释放
                    time.sleep(2.0)
                # 机械臂移动到作业准备点
                self.robot_motion(self.rbt, p_prepare, motion_type=motion, vel=100.0)
                
        else:
            raise ValueError("[参数错误]无效的堆叠方式,必须是'load'或'unload'")

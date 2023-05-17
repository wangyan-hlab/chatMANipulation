import time
import numpy as np
import sys
sys.path.append("../")
from fr_python_sdk.frrpc import RPC

class FRCobot(object):
    """
        FR Cobot Movement Control Wrapper

        Author: wangyan
        Date: 2023/05/12
    """

    def __init__(self, ip="192.168.58.2") -> None:
        
        self.robot = RPC(ip)
        
    def ResetAllError(self):
        """
        功能: 尝试清除错误状态,只能清除可复位的错误
        """
        resetallerror_ret = self.robot.ResetAllError() 
        time.sleep(1.0)
        if resetallerror_ret != 0:
            print("无法清除错误状态,错误不可复位,错误码:", resetallerror_ret)
        else:
            print("错误状态已清除,机器人成功复位")

    def JointJog(self, joint_num, joint_angle, 
                 vel=50.0, acc=50.0, max_dis=5.0, stop_mode="stopjog"):
        """
        功能: 控制机器人关节joint_num连续点动,旋转给定角度joint_angle

        参数:
            joint_num ('int'): 
                要旋转的关节编号, 可选[1,2,3,4,5,6]
            joint_angle ('float'): 
                旋转角度, 可指定正负, 单位: deg
            vel ('float'): 
                运动速度百分比, 0.0~100.0, 单位: %
            acc ('float'): 
                运动加速度百分比, 0.0~100.0, 单位: %
            max_dis ('float'): 
                单次点动最大角度, 单位: deg
            stop_mode ('str'): 
                “stopjog”: jog点动减速停止
                “immstopjog”: jog点动立即停止
        """

        ref = 0 # 关节点动
        dir = 1 if joint_angle > 0.0 else 0 # 旋转方向
        vel = float(vel)
        acc = float(acc)
        max_dis = float(max_dis)
        if max_dis <= 0.0:
            raise ValueError("max_dis must be greater than 0.0") # 单次点动最大角度必须为正
        loop_num = int(abs(joint_angle)//max_dis) if abs(joint_angle)%max_dis==0.0 \
            else int(abs(joint_angle)//max_dis)+1 # 计算点动次数
        
        for _ in range(loop_num):
            startjog_ret = self.robot.StartJOG(ref, joint_num, dir, vel, acc, max_dis)
            time.sleep(0.5*max_dis)
            if startjog_ret != 0:
                print("StartJOG 失败,错误码:", startjog_ret)
                self.ResetAllError() # 尝试清除错误状态
                return  # StartJOG()失败则直接结束
            if stop_mode == "stopjog":
                stopjog_ret = self.robot.StopJOG(1)
                time.sleep(1.0) 
                if stopjog_ret != 0:
                    print("StopJOG 失败,错误码:", stopjog_ret)
                    self.ResetAllError() # 尝试清除错误状态
                    return # StopJOG()失败则直接结束
            elif stop_mode == "immstopjog":
                immstopjog_ret = self.robot.ImmStopJOG()
                time.sleep(1.0)
                if immstopjog_ret != 0:
                    print("ImmStopJOG 失败,错误码:", immstopjog_ret)
                    self.ResetAllError() # 尝试清除错误状态
                    return # ImmStopJOG()失败则直接结束
        print("JointJOG 运行成功")

    def CartJog(self, frame, dim, dis, 
                vel=50.0, acc=50.0, max_dis=5.0, stop_mode="stopjog"):
        """
        功能: 在frame坐标系下,控制机器人在给定运动自由度dim上连续点动,运动给定距离/旋转给定角度dis

        参数:
            frame ('str'): 
                "base": 基坐标系点动
                "tool": 工具坐标系点动
                "wobj": 工件坐标系点动
            dim ('int'):
                运动自由度: 1~6分别对应"x","y","z","rx","ry","rz" 
            dis ('float'): 
                运动距离/旋转角度, 可指定正负, 单位: mm或deg
            vel ('float'): 
                运动速度百分比, 0.0~100.0, 单位: %
            acc ('float'): 
                运动加速度百分比, 0.0~100.0, 单位: %
            max_dis ('float'): 
                单次点动最大距离/角度, 单位: mm或deg
            stop_mode ('str'): 
                “stopjog”: jog点动减速停止
                “immstopjog”: jog点动立即停止
        """
        
        dis = float(dis)
        vel = float(vel)
        acc = float(acc)
        max_dis = float(max_dis)
        if frame == "base":
            ref = 2 # 基坐标系点动
        elif frame == "tool":
            ref = 4 # 工具坐标系点动
        elif frame == "wobj":
            ref = 8 # 工件坐标系点动
        else:
            raise ValueError("无效的关键字")
        dir = 1 if dis > 0.0 else 0 # 运动方向
        if max_dis <= 0.0:
            raise ValueError("max_dis must be greater than 0.0") # 单次点动最大角度必须为正
        loop_num = int(abs(dis)//max_dis) if abs(dis)%max_dis==0.0 \
            else int(abs(dis)//max_dis)+1 # 计算点动次数
        
        for _ in range(loop_num):
            startjog_ret = self.robot.StartJOG(ref, dim, dir, vel, acc, max_dis)
            time.sleep(0.5*max_dis)
            if startjog_ret != 0:
                print("StartJOG 失败,错误码:", startjog_ret)
                self.ResetAllError() # 尝试清除错误状态
                return  # StartJOG()失败则直接结束
            if stop_mode == "stopjog":
                stopjog_ret = self.robot.StopJOG(1)
                time.sleep(1.0) 
                if stopjog_ret != 0:
                    print("StopJOG 失败,错误码:", stopjog_ret)
                    self.ResetAllError() # 尝试清除错误状态
                    return # StopJOG()失败则直接结束
            elif stop_mode == "immstopjog":
                immstopjog_ret = self.robot.ImmStopJOG()
                time.sleep(1.0)
                if immstopjog_ret != 0:
                    print("ImmStopJOG 失败,错误码:", immstopjog_ret)
                    self.ResetAllError() # 尝试清除错误状态
                    return # ImmStopJOG()失败则直接结束
        print("CartJOG 运行成功")

    def MoveJ(self, target_pos, target_flag="joint", 
              vel=50.0, ovl=100.0, exaxis_pos=[0.0, 0.0, 0.0, 0.0], blendT=-1.0, 
              offset_flag=0, offset_pos=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
        """
        功能: 控制机器人关节空间运动到目标位置

        参数:
            target_pos ('list[float]'): 
                target_flag="joint"时, 表示目标关节位置, [j1,j2,j3,j4,j5,j6], 单位: deg;
                target_flag="desc"时, 表示目标笛卡尔位姿, [x,y,z,rx,ry,rz], 单位: mm
            target_flag ('str'):
                "joint": 目标用关节位置表示
                "desc": 目标用笛卡尔位姿表示
            vel ('float'): 
                运动速度百分比, 0.0~100.0, 单位: %
            ovl ('float'): 
                速度缩放因子, 0.0~100.0, 单位: %
            exaxis_pos ('numpy.ndarray'): 
                外部轴1位置~外部轴4位置,单位mm
            blendT ('float'):
                -1.0: 运动到位(阻塞) 
                0~500: 平滑时间(非阻塞), 单位: ms
            offset_flag ('int'):
                0: 不偏移
                1: 工件/基坐标系下偏移
                2: 工具坐标系下偏移
            offset_pos ('numpy.ndarray'):
                位姿偏移量，单位:mm和°
        """

        vel = float(vel)
        ovl = float(ovl)
        blendT = float(blendT)
        acc = 0.0   # 加速度百分比，暂不开放，默认为0.0
        tool = self.robot.GetActualTCPNum(0)[1]
        user = self.robot.GetActualWObjNum(0)[1]
        
        if target_flag == "joint":
            target_joint_pos = target_pos
            getfk_ret = self.robot.GetForwardKin(target_joint_pos) # 计算目标位姿
            if getfk_ret[0] == 0:
                target_desc_pos = getfk_ret[1:]
                print("正运动学求解成功,目标笛卡尔位姿为:", target_desc_pos)
            else:
                print("正运动学求解失败,错误码:", getfk_ret[0])
                self.ResetAllError() # 尝试清除错误状态
                return # GetForwardKin()失败则直接结束
        elif target_flag == "desc":
            target_desc_pos = target_pos
            joint_pos_ref = self.robot.GetActualJointPosDegree(0)[1:]
            #TODO:这里需要纠错，文档中GetInverseKinHasSolution()缺少第一个参数0
            ik_has_solution = self.robot.GetInverseKinHasSolution(0, target_desc_pos, joint_pos_ref)
            if ik_has_solution[0] == 0:
                if ik_has_solution[1]:
                    #TODO:这里需要纠错，文档中GetInverseKinRef()缺少第一个参数0
                    getikref_ret = self.robot.GetInverseKinRef(0, target_desc_pos, joint_pos_ref)
                    if getikref_ret[0] == 0:
                        target_joint_pos = getikref_ret[1:]
                        print("逆运动学求解成功,目标关节位置为:", target_joint_pos)
                    else:
                        print("逆运动学求解失败,错误码:", getikref_ret[0])
                        self.ResetAllError() # 尝试清除错误状态
                        return # GetInverseKinHasSolution()失败则直接结束
                else:
                    getikref_ret = self.robot.GetInverseKinRef(0, target_desc_pos, joint_pos_ref)
                    print("逆运动学求解失败,错误码:", getikref_ret[0])
                    self.ResetAllError() # 尝试清除错误状态
                    return # GetInverseKinHasSolution()失败则直接结束
            else:
                print("逆运动学求解失败,错误码:", ik_has_solution[0])
                self.ResetAllError() # 尝试清除错误状态
                return # GetInverseKinRef()失败则直接结束
        else:
            raise ValueError("无效的关键字")

        movej_ret = self.robot.MoveJ(target_joint_pos, target_desc_pos, tool, user, 
                         vel, acc, ovl, exaxis_pos, blendT, offset_flag, offset_pos)
        if movej_ret != 0:
            print("MoveJ 失败,错误码:", movej_ret)
            self.ResetAllError() # 尝试清除错误状态
            return # MoveJ()失败则直接结束
        print("MoveJ 运行成功")
    
    def MoveL(self, target_pos, target_flag="joint", 
              vel=50.0, ovl=100.0, exaxis_pos=[0.0, 0.0, 0.0, 0.0], blendR=-1.0, 
              search=0, offset_flag=0, offset_pos=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
        """
        功能: 控制机器人笛卡尔空间直线运动到目标位置

        参数:
            target_pos ('list[float]'): 
                target_flag="joint"时, 表示目标关节位置, [j1,j2,j3,j4,j5,j6], 单位: deg;
                target_flag="desc"时, 表示目标笛卡尔位姿, [x,y,z,rx,ry,rz], 单位: mm
            target_flag ('str'):
                "joint": 目标用关节位置表示
                "desc": 目标用笛卡尔位姿表示
            vel ('float'): 
                运动速度百分比, 0.0~100.0, 单位: %
            ovl ('float'): 
                速度缩放因子, 0.0~100.0, 单位: %
            exaxis_pos ('numpy.ndarray'): 
                外部轴1位置~外部轴4位置,单位mm
            blendR ('double'):
                -1.0: 运动到位(阻塞)
                0~500: 平滑时间(非阻塞), 单位: ms
            search ('int'):
                0: 不焊丝寻位
                1: 焊丝寻位
            offset_flag ('int'):
                0: 不偏移
                1: 工件/基坐标系下偏移
                2: 工具坐标系下偏移
            offset_pos ('numpy.ndarray'):
                位姿偏移量，单位:mm和°
        """

        vel = float(vel)
        ovl = float(ovl)
        blendR = float(blendR)
        acc = 0.0   # 加速度百分比，暂不开放，默认为0.0
        tool = self.robot.GetActualTCPNum(0)[1]
        user = self.robot.GetActualWObjNum(0)[1]
        
        if target_flag == "joint":
            target_joint_pos = target_pos
            getfk_ret = self.robot.GetForwardKin(target_joint_pos) # 计算目标位姿
            if getfk_ret[0] == 0:
                target_desc_pos = getfk_ret[1:]
                print("正运动学求解成功,目标笛卡尔位姿为:", target_desc_pos)
            else:
                print("正运动学求解失败,错误码:", getfk_ret[0])
                self.ResetAllError() # 尝试清除错误状态
                return # GetForwardKin()失败则直接结束
        elif target_flag == "desc":
            target_desc_pos = target_pos
            joint_pos_ref = self.robot.GetActualJointPosDegree(0)[1:]
            ik_has_solution = self.robot.GetInverseKinHasSolution(0, target_desc_pos, joint_pos_ref)
            if ik_has_solution[0] == 0:
                if ik_has_solution[1]:
                    getikref_ret = self.robot.GetInverseKinRef(0, target_desc_pos, joint_pos_ref)
                    if getikref_ret[0] == 0:
                        target_joint_pos = getikref_ret[1:]
                        print("逆运动学求解成功,目标关节位置为:", target_joint_pos)
                    else:
                        print("逆运动学求解失败,错误码:", getikref_ret[0])
                        self.ResetAllError() # 尝试清除错误状态
                        return # GetInverseKinHasSolution()失败则直接结束
                else:
                    getikref_ret = self.robot.GetInverseKinRef(0, target_desc_pos, joint_pos_ref)
                    print("逆运动学求解失败,错误码:", getikref_ret[0])
                    self.ResetAllError() # 尝试清除错误状态
                    return # GetInverseKinHasSolution()失败则直接结束
            else:
                print("逆运动学求解失败,错误码:", ik_has_solution[0])
                self.ResetAllError() # 尝试清除错误状态
                return # GetInverseKinRef()失败则直接结束
        else:
            raise ValueError("无效的关键字")

        movel_ret = self.robot.MoveL(target_joint_pos, target_desc_pos, tool, user, 
                         vel, acc, ovl, blendR, exaxis_pos, search, offset_flag, offset_pos)
        if movel_ret != 0:
            print("MoveJ 失败,错误码:", movel_ret)
            self.ResetAllError() # 尝试清除错误状态
            return # MoveL()失败则直接结束
        print("MoveL 运行成功")

# FR Cobot Movement Control Wrapper Test
#
# author: wangyan
# date: 2023/05/17

# %%
import numpy as np
import sys
sys.path.append("../")
from frmovewrapper.frmove import FRCobot

rbt = FRCobot()

# %% 
# JointJog() test 1 pass
rbt.GetJointPos()
rbt.JointJog(joint_num=1, joint_angle=10)
rbt.GetJointPos()

# %%
# JointJog() test 2 pass
rbt.GetJointPos()
rbt.JointJog(joint_num=1, joint_angle=-10, max_dis=10)
rbt.GetJointPos()

# %%
# JointJog() test 3 pass
rbt.GetJointPos()
rbt.JointJog(joint_num=1, joint_angle=10, vel=100.0, max_dis=10, stop_mode="immstopjog")
rbt.GetJointPos()

# %%
# CartJog() test 1 pass
rbt.GetTCPPose()
rbt.CartJog(frame="base", dim=3, dis=20)
rbt.GetTCPPose()

# %%
# CartJog() test 2 pass
rbt.GetTCPPose()
print("当前工具坐标系编号:", rbt.GetFrameNum())
rbt.CartJog(frame="tool", dim=3, dis=20, vel=100.0, max_dis=10)
rbt.GetTCPPose()

# %%
# MoveJ() test 1 pass
start_jnt_pos = rbt.GetJointPos()
delta_jnt_pos = np.array([-10,0,0,0,0,0])
target_jnt_pos = list(np.asarray(start_jnt_pos) + delta_jnt_pos)
for i in range(6):
    target_jnt_pos[i] = float(target_jnt_pos[i])  # 需要使用built-in float

rbt.MoveJ(target_jnt_pos, target_flag="joint")
start_jnt_pos = rbt.GetJointPos()

# %%
# MoveJ() test 2 pass
start_tcp_pos = rbt.GetTCPPose()
print(start_tcp_pos)
delta_tcp_pos = np.array([10,0,0,0,0,0])
target_tcp_pos = list(np.asarray(start_tcp_pos) + delta_tcp_pos)
for i in range(6):
    target_tcp_pos[i] = float(target_tcp_pos[i])  # 需要使用built-in float

rbt.MoveJ(target_tcp_pos, target_flag="desc")
rbt.GetTCPPose()

# %%
# MoveL() test 1
start_jnt_pos = rbt.GetJointPos()
delta_jnt_pos = np.array([10,0,0,0,0,0])
target_jnt_pos = list(np.asarray(start_jnt_pos) + delta_jnt_pos)
for i in range(6):
    target_jnt_pos[i] = float(target_jnt_pos[i])  # 需要使用built-in float

rbt.MoveL(target_jnt_pos, target_flag="joint")
rbt.GetJointPos()

# %%
# MoveL() test 2
start_tcp_pos = rbt.GetTCPPose()
delta_tcp_pos = np.array([-10,0,0,0,0,0])
target_tcp_pos = list(np.asarray(start_tcp_pos) + delta_tcp_pos)
for i in range(6):
    target_tcp_pos[i] = float(target_tcp_pos[i])  # 需要使用built-in float

rbt.MoveL(target_tcp_pos, target_flag="desc")
rbt.GetTCPPose()

# %%

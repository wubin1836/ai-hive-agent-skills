# 离线检查器

item_mm与opening_mm均为毫米正整数，total_clearance_mm为单个开口宽或高维度的总余量（不是每侧余量）。allowed_orientations必须由用户/厂家允许，三轴次序为占用开口宽、开口高、行进深度。计算每个允许朝向的占宽+总余量≤净开口宽且占高+总余量≤净开口高。深度、转角、倾斜、安全姿态、人员空间和安装间距不在模型内；full_route_verdict始终not_assessed。二维不通过不代表所有三维搬运方式都不可能，通过也绝不代表整条路径通过。

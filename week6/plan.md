# plan

- 扩展 locaterunway 的功能，使其支持多个文件的上传和下载。
- 对比仿真的 SAR 与原图，得到灰度差异
- 问题：仿真的图像区域增长法无法通用实现，现有办法是不是有点慢呢
- 问题：找不到 SAR 对应的原图

- 整合 locaterunway 仿真 sar 图像和 anotherapp 打击效果仿真的功能，实现光学图像图像的 SAR 打击效果仿真

- 图像配准变化检测毁伤评估
- 问题：如何进行图像配准
  - 仿射变换
  采用人工选择控制点的方法对打击前后图像进行配准
  I)在打击前图像上选取3个特征点，要求特征点较明显，易于在打击后图像上找到其对应的点；
  II)在打击后图像上选择相应的特征点；
  III)将两组点代入仿射变换模型，计算仿射变换参数；
  IV)根据仿射变换参数，对打击后图像进行重采样，得到已配准的图像。
- 问题：如何进行变化检测
  具体算法步骤为：
  I)计算配准后的两幅图像对应位置点的差值，得到差值结果图。对应点的灰度值取该点55×领域内像素的均值。
  II)对差值结果做进一步的均值滤波，减小图像噪声的影响。
  III)对均值滤波结果根据式（3-11）进行阈值分割，阈值dT取1，得到初步的变化检测结果。
  IV)对初步的变化检测结果进行形态学膨胀、腐蚀操作，通过区域标记法滤除小区域，得到真实变化毁伤区域。
- 问题：如何进行毁伤评估
  对SAR图像进行打击效果评估。毁伤评估准则如下:1级毁伤：1.5(  ,   )Ixyσ>≥σ（无毁伤或者轻微毁伤）2级毁伤：2(,)1.5Ixyσ>≥  σ（轻微毁伤或者中度毁伤）3级毁伤：2.5(  ,   )    2Ixyσ>≥ σ（中度毁伤或者严重毁伤）4级毁伤：(, )  2.5Ixy≥σ（严重毁伤或者完全毁伤）

主要在第四章各个小章节
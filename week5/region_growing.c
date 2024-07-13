#include <stdbool.h>
#include <stdlib.h>

void region_growing(unsigned char* img, int rows, int cols, int seedX, int seedY, unsigned char threshold) {
  bool* visited = (bool*)calloc(rows * cols, sizeof(bool));
  int dx[4] = {-1, 0, 1, 0};
  int dy[4] = {0, 1, 0, -1};

  // 使用一个简单的数组模拟队列
  int* queueX = (int*)malloc(rows * cols * sizeof(int));
  int* queueY = (int*)malloc(rows * cols * sizeof(int));
  int queue_start = 0, queue_end = 0;

  // 添加种子点到队列
  queueX[queue_end] = seedX;
  queueY[queue_end] = seedY;
  queue_end++;

  unsigned char seed_value = img[seedY * cols + seedX];

  while (queue_start < queue_end) {
    int x = queueX[queue_start];
    int y = queueY[queue_start];
    queue_start++;

    if (!visited[y * cols + x] && abs(img[y * cols + x] - seed_value) <= threshold) {
      visited[y * cols + x] = true;
      img[y * cols + x] = 0; // 标记为访问

      for (int i = 0; i < 4; i++) {
        int nx = x + dx[i];
        int ny = y + dy[i];

        if (0 <= nx && nx < cols && 0 <= ny && ny < rows) {
          queueX[queue_end] = nx;
          queueY[queue_end] = ny;
          queue_end++;
        }
      }
    }
  }

  free(visited);
  free(queueX);
  free(queueY);
}
w = [0.3;0.5;0.5];
learning_rate = 1;
X = [-1, 0, 0; -1, 0, 1; -1, 1, 0; -1, 1, 1];
Y = [1; 1; 0; 0];
counter = 0;
errors = [];
while counter < 10
  epoch_error = 0;
  for i = 1:size(X, 1)
    s = custom_sign(w' * X(i, :)');
    if (Y(i) - s) ~= 0
      w = w + learning_rate * (Y(i) - s) * X(i, :)';
      epoch_error = epoch_error + abs(Y(i) - s);
    end
  end
  errors = [errors; epoch_error];
  counter = counter + 1;
end
disp(w)
plot(errors)
xlabel('Epoch')
ylabel('Error')
s1 = custom_sign(w' * X(1, :)');
s2 = custom_sign(w' * X(2, :)');
s3 = custom_sign(w' * X(3, :)');
s4 = custom_sign(w' * X(4, :)');
figure
hold on
plot_point(X(1, :), s1);
plot_point(X(2, :), s2);
plot_point(X(3, :), s3);
plot_point(X(4, :), s4);
x_values = linspace(min([X(1, 1), X(2, 1), X(3, 1), X(4, 1)]), max([X(1, 1), X(2, 1), X(3, 1), X(4, 1)]), 100);
y_values = -((w(1) * x_values) + w(2)) / w(3);
plot(x_values, y_values, 'k')
xlabel('X1')
ylabel('X2')
legend('Class 1', 'Class 2')
hold off
function plot_point(X, s)
    if s == 1
        plot(X(2), X(3), 'bo')
    else
        plot(X(2), X(3), 'ro')
    end
end
function y = custom_sign(x)
  if x >= 0
    y = 1;
  else
    y = 0;
  end
end
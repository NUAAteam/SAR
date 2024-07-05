% Initialize weights
w = [0.3;0.5;0.5];

% Set the learning rate
learning_rate = 1;

% Define the samples and target outputs
X = [-1, 0, 0; -1, 0, 1; -1, 1, 0; -1, 1, 1];
Y = [1; 1; 0; 0];

% Initialize the counter and the error array
counter = 0;
errors = [];

% Train the perceptron
while counter < 10
  weight_updated = false;
  epoch_error = 0;
  for i = 1:size(X, 1)
    % Compute the output
    s = custom_sign(w' * X(i, :)');

    % Check if the output is not equal to the target output
    if (Y(i) - s) ~= 0
      % Update the weights
      w = w + learning_rate * (Y(i) - s) * X(i, :)';
      weight_updated = true;

      % Update the epoch error
      epoch_error = epoch_error + abs(Y(i) - s);
    end
  end

  % Record the epoch error
  errors = [errors; epoch_error];

  % If the weights were not updated in this epoch, break the loop
  if ~weight_updated
    break;
  end

  % Increment the counter
  counter = counter + 1;
end

% Display the trained weights
disp(w)

% Plot the error over time
plot(errors)
xlabel('Epoch')
ylabel('Error')

s1=custom_sign(w'*X(1,:)')
s2=custom_sign(w'*X(2,:)')
s3=custom_sign(w'*X(3,:)')
s4=custom_sign(w'*X(4,:)')
% Create a new figure

% Define the data points
X1 = X(1, :);
X2 = X(2, :);
X3 = X(3, :);
X4 = X(4, :);
figure
hold on

% Plot the data points
if s1 == 1
    plot(X1(2), X1(3), 'bo')
else
    plot(X1(2), X1(3), 'ro')
end

if s2 == 1
    plot(X2(2), X2(3), 'bo')
else
    plot(X2(2), X2(3), 'ro')
end

if s3 == 1
    plot(X3(2), X3(3), 'bo')
else
    plot(X3(2), X3(3), 'ro')
end

if s4 == 1
    plot(X4(2), X4(3), 'bo')
else
    plot(X4(2), X4(3), 'ro')
end

% Plot the decision boundary
x_values = linspace(min([X1(1), X2(1), X3(1), X4(1)]), max([X1(1), X2(1), X3(1), X4(1)]), 100);

y_values = -((w(1) * x_values) + w(2)) / w(3);
plot(x_values, y_values, 'k')

% Set the plot labels and legend
xlabel('X1')
ylabel('X2')
legend('Class 1', 'Class 2')

hold off

% Custom sign function


function y = custom_sign(x)
  if x >= 0
    y = 1;
  else
    y = 0;
  end
end


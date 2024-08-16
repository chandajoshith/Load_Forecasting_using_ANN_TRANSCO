% Load data
data = readtable('load_data_5.csv');
dates = data.Date;
loads = data.Load;
temperatures = data.Temperature;

% Convert dates to numeric for use in the ANN
dateNums = datenum(dates);

% Prepare data for training
X = [dateNums, temperatures];
Y = loads;

% Create and train the neural network
hiddenLayerSize = 10; % Number of neurons in the hidden layer
net = fitnet(hiddenLayerSize);

% Set up Division of Data for Training, Validation, and Testing
net.divideParam.trainRatio = 99/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;

% Train the network
[net, tr] = train(net, X', Y');

% Predict future data
% Generate future dates (next 3 years)
futureDates = (max(dateNums) + (1:365*3))';
futureTemperatures = mean(temperatures) * ones(length(futureDates), 1); % Assuming constant temperature for simplicity
futureInputs = [futureDates, futureTemperatures];

% Predict future loads
futureLoads = net(futureInputs');

% Convert future dates back to datetime format for plotting
futureDates = datetime(futureDates, 'ConvertFrom', 'datenum');

% Convert numeric dates back to datetime format for plotting
dates = datetime(dateNums, 'ConvertFrom', 'datenum');

% Plot historical and predicted data
figure;
hold on;
plot(dates, loads, 'b', 'DisplayName', 'Historical Load Data');
plot(futureDates, futureLoads, 'r--', 'DisplayName', 'Predicted Load Data');
xlabel('Date');
ylabel('Load');
legend;
title('Load Data and Forecast');
grid on;

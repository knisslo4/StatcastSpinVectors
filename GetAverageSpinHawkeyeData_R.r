# Load Libraries
library(dplyr)
library(readr)

# Load Data
data <- read_csv('verlander_ff_2023.csv')
df <- data %>% select(release_speed, spin_axis, vx0, vy0, vz0)
head(df)

# Compute Averages
velocity <- mean(df$release_speed)
spin_axis <- mean(df$spin_axis)
vx <- mean(df$vx0)
vy <- mean(df$vy0)
vz <- mean(df$vz0)
spin_eff <- 0.96

print(velocity)
print(spin_axis)
print(vx)
print(vy)
print(vz)
print(spin_eff)

# Define Functions
cal_unit_velocity_vector <- function(vx, vy, vz, velocity) {
  vx_v <- vx / velocity
  vy_v <- vy / velocity
  vz_v <- vz / velocity
  return(c(vx_v, vy_v, vz_v))
}

cal_vert_release_ang <- function(vx, vy) {
  vert_release_ang <- atan(vx / vy)
  return(vert_release_ang)
}

cal_horz_release_ang <- function(vz, velocity) {
  horz_release_ang <- asin(vz / velocity)
  return(horz_release_ang)
}

cal_cosine_angle <- function(spin_axis) {
  if (spin_axis > 90) {
    cosine_angle <- -sqrt(1 - spin_eff^2)
  } else {
    cosine_angle <- sqrt(1 - spin_eff^2)
  }
  return(cosine_angle)
}

# Calculate Intermediate Values
unit_velocity_vector <- cal_unit_velocity_vector(vx, vy, vz, velocity)
vx_v <- unit_velocity_vector[1]
vy_v <- unit_velocity_vector[2]
vz_v <- unit_velocity_vector[3]

vert_release_ang <- cal_vert_release_ang(vx, vy)
horz_release_ang <- cal_horz_release_ang(vz, velocity)
cosine_angle <- cal_cosine_angle(spin_axis)

print(vx_v)
print(vy_v)
print(vz_v)
print(vert_release_ang)
print(horz_release_ang)
print(cosine_angle)

# Calculate Polar Angle
A <- vx_v * cos(spin_axis) + vz_v * sin(spin_axis)
C <- cosine_angle
B <- vy_v
R <- sqrt(A^2 + B^2)
X <- atan(B / A)
polar_angle <- asin(C / R) - X

print(A)
print(B)
print(C)
print(R)
print(X)
print(polar_angle)

# Calculate Angular Velocities
wx <- sin(polar_angle) * cos(spin_axis)
wy <- cos(polar_angle)
wz <- sin(horz_release_ang) * sin(spin_axis)

print(wx)
print(wy)
print(wz)
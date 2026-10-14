# Perfil longitudinal de Oxígeno Disuelto — resultados QUAL2K
# Datos extraídos de Escenario_Prueba.out (sección "Water Quality Summary")
# Columnas usadas: x (km) y DO (mgO2/L)

library(ggplot2)

# ---- Datos: distancia aguas abajo (km) y Oxígeno Disuelto (mg/L) ----
df <- data.frame(
  x_km     = c(13.600000, 13.387500, 12.962500, 12.325000, 11.475000,
               10.625000,  9.775000,  8.925000,  8.075000,  7.225000,
                6.375000,  5.525000,  4.675000,  3.825000,  2.975000,
                2.125000,  1.275000,  0.425000,  0.000000),
  do_mgl   = c(8.280976, 5.231935, 4.778800, 4.325261, 4.147807,
               4.129311, 3.694387, 4.204600, 4.602250, 4.923123,
               5.064940, 5.689236, 6.144276, 6.478045, 6.729394,
               6.925225, 7.082888, 7.213410, 7.213410),
  etiqueta = c("Cabecera", "MP 0.4", "", "", "", "", "", "", "MP 3.5",
               "", "", "", "", "MP 5.6", "", "", "", "", "Terminus")
)

# Punto crítico de caída (sag): mínimo de OD
sag <- df[which.min(df$do_mgl), ]

p <- ggplot(df, aes(x = x_km, y = do_mgl)) +
  # Límite de hipoxia
  geom_hline(yintercept = 4.0, linetype = "dashed", color = "red", linewidth = 0.7) +
  annotate("text", x = 13.45, y = 4.14, hjust = 0, size = 3.4, color = "red",
           label = "Límite de hipoxia (4.0 mg/L)") +
  # Serie de datos: línea sólida + puntos en cada tramo
  geom_line(color = "#1f78b4", linewidth = 0.9) +
  geom_point(color = "#1f78b4", size = 2.6) +
  # Punto crítico del sag resaltado
  geom_point(data = sag, shape = 24, color = "red", fill = "yellow",
             size = 5, stroke = 1.1) +
  annotate("text", x = 8.85, y = 3.42, hjust = 0, size = 3.4,
           color = "darkred", fontface = "bold",
           label = sprintf("Mínimo del sag: %.2f mg/L\nkm %.2f", sag$do_mgl, sag$x_km)) +
  # Etiquetas de puntos de monitoreo
  geom_text(data = df[df$etiqueta != "", ], aes(label = etiqueta),
            size = 3.1, color = "grey25", vjust = -1.1) +
  # Flecha de dirección del flujo
  annotate("segment", x = 12.95, xend = 12.25, y = 8.55, yend = 8.55,
           arrow = arrow(length = unit(0.12, "inches"), type = "closed"),
           color = "grey25", linewidth = 0.6) +
  annotate("text", x = 12.6, y = 8.66, size = 3.1, color = "grey25",
           label = "Dirección del flujo") +
  # Eje X invertido: cabecera (km 13.6) a la izquierda, desembocadura (km 0) a la derecha
  scale_x_reverse(limits = c(0, 13.9), expand = expansion(mult = 0.01)) +
  scale_y_continuous(limits = c(3.2, 8.9), expand = expansion(mult = c(0.02, 0.03))) +
  labs(
    title = "Perfil longitudinal de Oxígeno Disuelto",
    subtitle = "Escenario_Prueba.q2k — simulación QUAL2K v3.00b8 (Boulder Creek, 21/8/1987)",
    x = "Distancia (km)",
    y = "Oxígeno Disuelto (mg/L)",
    caption = "Fuente: Escenario_Prueba.out (Water Quality Summary) · Eje X en dirección del flujo: cabecera (km 13.6) → desembocadura (km 0)"
  ) +
  theme_classic(base_size = 12) +
  theme(
    plot.title    = element_text(face = "bold", size = 14, color = "black"),
    plot.subtitle = element_text(size = 10, color = "grey25"),
    axis.title    = element_text(face = "bold", color = "black"),
    axis.text     = element_text(color = "black"),
    plot.caption  = element_text(size = 8.5, color = "grey25")
  )

# ---- Guardado en alta resolución ----
ggsave(
  filename = "C:/Users/majur/Downloads/Perfil_Oxigeno_QUAL2K.png",
  plot     = p,
  width    = 10,
  height   = 6,
  units    = "in",
  dpi      = 300,
  bg       = "white"
)

cat("Gráfico guardado en: C:/Users/majur/Downloads/Perfil_Oxigeno_QUAL2K.png\n")
cat("Punto sag (mínimo): x =", sag$x_km, "km, DO =", sag$do_mgl, "mg/L\n")

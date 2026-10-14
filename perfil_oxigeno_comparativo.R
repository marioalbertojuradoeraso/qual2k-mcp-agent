# Perfil longitudinal de Oxígeno Disuelto — QUAL2K (comparativo)
# Base: HO04Q2KpHSOD.out   vs   Remediación: Escenario_Remediacion.out
# (WWTP: CBOD 13.35 -> 6.675 mg/L y NH4 5000 -> 2500 ugN/L, -50 %)
# Lee los CSV extraídos del 'Water Quality Summary' vía MCP.

library(ggplot2)

base <- read.csv("C:/Users/majur/QUAL2K/curva_do_base.csv")
reme <- read.csv("C:/Users/majur/QUAL2K/curva_do_remediacion.csv")

base$escenario <- "Base (HO04Q2KpHSOD)"
reme$escenario <- "Remediación (WWTP -50 % CBOD/NH4)"
df <- rbind(base, reme)

# Etiquetas de monitoreo por posición kilométrica
df$etiqueta <- ""
df$etiqueta[df$x_km == 13.6]    <- "Cabecera"
df$etiqueta[df$x_km == 13.3875] <- "MP 0.4 (WWTP)"
df$etiqueta[df$x_km == 8.075]   <- "MP 3.5"
df$etiqueta[df$x_km == 3.825]   <- "MP 5.6"
df$etiqueta[df$x_km == 0.0]     <- "Terminus"

# Puntos críticos del sag (mínimo de OD por escenario)
sag_base <- base[which.min(base$do_mgl), ]
sag_reme <- reme[which.min(reme$do_mgl), ]

col_base <- "#d7301f"  # rojo: escenario base
col_reme <- "#1f78b4"  # azul: escenario remediado

p <- ggplot(df, aes(x = x_km, y = do_mgl, color = escenario, group = escenario)) +
  # Límite de hipoxia
  geom_hline(yintercept = 4.0, linetype = "dashed", color = "red", linewidth = 0.7) +
  annotate("text", x = 13.45, y = 4.14, hjust = 0, size = 3.4, color = "red",
           label = "Límite de hipoxia (4.0 mg/L)") +
  # Curvas + puntos
  geom_line(linewidth = 0.9) +
  geom_point(size = 2.4) +
  # Sags resaltados
  geom_point(data = sag_base, aes(x = x_km, y = do_mgl),
             shape = 24, color = "darkred", fill = "yellow", size = 5, stroke = 1.1,
             inherit.aes = FALSE) +
  geom_point(data = sag_reme, aes(x = x_km, y = do_mgl),
             shape = 24, color = "darkgreen", fill = "yellow", size = 5, stroke = 1.1,
             inherit.aes = FALSE) +
  annotate("text", x = 8.85, y = 3.40, hjust = 0, size = 3.4,
           color = "darkred", fontface = "bold",
           label = sprintf("Sag base: %.2f mg/L (km %.2f)", sag_base$do_mgl, sag_base$x_km)) +
  annotate("text", x = 8.85, y = 4.32, hjust = 0, size = 3.4,
           color = "darkgreen", fontface = "bold",
           label = sprintf("Sag remediado: %.2f mg/L (km %.2f)", sag_reme$do_mgl, sag_reme$x_km)) +
  # Etiquetas de monitoreo (solo una capa para no duplicar)
  geom_text(data = df[df$etiqueta != "" & df$escenario == "Base (HO04Q2KpHSOD)", ],
            aes(label = etiqueta), color = "grey25", size = 3.0, vjust = -1.1,
            show.legend = FALSE) +
  # Flecha de dirección del flujo (debajo del punto de cabecera para no solaparse)
  annotate("segment", x = 12.95, xend = 12.25, y = 7.95, yend = 7.95,
           arrow = arrow(length = unit(0.12, "inches"), type = "closed"),
           color = "grey25", linewidth = 0.6) +
  annotate("text", x = 12.6, y = 8.08, size = 3.1, color = "grey25",
           label = "Dirección del flujo") +
  scale_color_manual(values = c("Base (HO04Q2KpHSOD)" = col_base,
                                "Remediación (WWTP -50 % CBOD/NH4)" = col_reme),
                     name = "Escenario") +
  # Eje X invertido: cabecera (km 13.6) a la izquierda, desembocadura a la derecha
  scale_x_reverse(limits = c(-0.55, 13.9), expand = expansion(mult = 0.01)) +
  scale_y_continuous(limits = c(3.2, 8.9), expand = expansion(mult = c(0.02, 0.03))) +
  labs(
    title = "Perfil longitudinal de Oxígeno Disuelto",
    subtitle = "Boulder Creek (21/8/1987) — QUAL2K v3.00b8 · Remediación: CBOD y NH4 del WWTP -50 %",
    x = "Distancia (km)",
    y = "Oxígeno Disuelto (mg/L)",
    caption = "Fuente: HO04Q2KpHSOD.out y Escenario_Remediacion.out (Water Quality Summary) · Eje X en dirección del flujo: cabecera (km 13.6) → desembocadura (km 0)"
  ) +
  theme_classic(base_size = 12) +
  theme(
    plot.title    = element_text(face = "bold", size = 14, color = "black"),
    plot.subtitle = element_text(size = 10, color = "grey25"),
    axis.title    = element_text(face = "bold", color = "black"),
    axis.text     = element_text(color = "black"),
    plot.caption  = element_text(size = 8.5, color = "grey25"),
    legend.position = "bottom"
  )

salida <- "C:/Users/majur/QUAL2K/Perfil_Oxigeno_Comparativo.png"
ggsave(filename = salida, plot = p, width = 10, height = 6,
       units = "in", dpi = 300, bg = "white")

cat("Gráfico guardado en:", salida, "\n")
cat(sprintf("Sag base: %.3f mg/L en km %.3f\n", sag_base$do_mgl, sag_base$x_km))
cat(sprintf("Sag remediado: %.3f mg/L en km %.3f\n", sag_reme$do_mgl, sag_reme$x_km))
cat(sprintf("Mejora: %+.3f mg/L\n", sag_reme$do_mgl - sag_base$do_mgl))

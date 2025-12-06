-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-12-2025 a las 16:15:46
-- Versión del servidor: 10.1.28-MariaDB
-- Versión de PHP: 5.6.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ganaderia_app`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `animal`
--

CREATE TABLE `animal` (
  `id_animal` int(11) NOT NULL,
  `arete` varchar(50) NOT NULL,
  `origen` enum('nacido','comprado') NOT NULL,
  `peso_inicial` decimal(10,2) DEFAULT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `raza` varchar(50) DEFAULT NULL,
  `observaciones` text,
  `id_lote` int(11) DEFAULT NULL,
  `id_proveedor` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `animal`
--

INSERT INTO `animal` (`id_animal`, `arete`, `origen`, `peso_inicial`, `fecha_ingreso`, `fecha_nacimiento`, `raza`, `observaciones`, `id_lote`, `id_proveedor`) VALUES
(1, 'ENG-001', 'comprado', '300.00', '2023-06-01', '2022-12-01', 'Angus Negro', 'Listo en 30 dias', 2, 1),
(2, 'ENG-002', 'comprado', '295.00', '2023-06-01', '2022-12-05', 'Angus Rojo', NULL, 2, 1),
(3, 'ENG-003', 'comprado', '310.00', '2023-06-01', '2022-12-10', 'Charolais', 'Excelente estructura', 2, 2),
(4, 'ENG-004', 'comprado', '305.00', '2023-06-01', '2022-12-12', 'Hereford', NULL, 2, 1),
(5, 'ENG-005', 'comprado', '290.00', '2023-06-01', '2022-12-15', 'Brahman', 'Temperamental', 2, 3),
(6, 'ENG-006', 'comprado', '320.00', '2023-06-01', '2022-11-20', 'Simmental', NULL, 2, 2),
(7, 'ENG-007', 'comprado', '315.00', '2023-06-01', '2022-11-25', 'Angus Negro', NULL, 2, 1),
(8, 'ENG-008', 'comprado', '300.00', '2023-06-01', '2022-12-01', 'Brangus', NULL, 2, 1),
(9, 'ENG-009', 'comprado', '285.00', '2023-06-01', '2022-12-05', 'Charolais', NULL, 2, 2),
(10, 'ENG-010', 'comprado', '330.00', '2023-06-01', '2022-11-10', 'Beefmaster', 'El más pesado', 2, 4),
(11, 'ENG-011', 'comprado', '305.00', '2023-06-01', '2022-12-08', 'Hereford', NULL, 2, 1),
(12, 'ENG-012', 'comprado', '298.00', '2023-06-01', '2022-12-14', 'Angus x Charolais', NULL, 2, 3),
(13, 'ENG-013', 'comprado', '312.00', '2023-06-01', '2022-11-30', 'Limousin', NULL, 2, 2),
(14, 'ENG-014', 'comprado', '308.00', '2023-06-01', '2022-12-02', 'Santa Gertrudis', NULL, 2, 4),
(15, 'ENG-015', 'comprado', '300.00', '2023-06-01', '2022-12-01', 'Brahman', NULL, 2, 1),
(16, 'DES-101', 'comprado', '180.00', '2023-08-15', '2023-02-01', 'Criollo', 'Ganado de oportunidad', 1, 3),
(17, 'DES-102', 'comprado', '185.00', '2023-08-15', '2023-02-05', 'Criollo', NULL, 1, 3),
(18, 'DES-103', 'comprado', '190.00', '2023-08-15', '2023-02-10', 'Cebuino', NULL, 1, 3),
(19, 'DES-104', 'comprado', '175.00', '2023-08-15', '2023-02-15', 'Cebuino', 'Cuernos largos', 1, 3),
(20, 'DES-105', 'comprado', '200.00', '2023-08-15', '2023-01-20', 'Sardo Negro', NULL, 1, 4),
(21, 'DES-106', 'comprado', '195.00', '2023-08-15', '2023-01-25', 'Gyr', NULL, 1, 4),
(22, 'DES-107', 'comprado', '188.00', '2023-08-15', '2023-02-01', 'Nelore', NULL, 1, 4),
(23, 'DES-108', 'comprado', '182.00', '2023-08-15', '2023-02-05', 'Brahman Rojo', NULL, 1, 1),
(24, 'DES-109', 'comprado', '192.00', '2023-08-15', '2023-02-08', 'Indubrasil', NULL, 1, 1),
(25, 'DES-110', 'comprado', '185.00', '2023-08-15', '2023-02-12', 'Suiz-Bu', NULL, 1, 1),
(26, 'NAC-201', 'nacido', '35.00', '2023-11-01', '2023-11-01', 'Angus', 'Hijo de vaca 404', 3, NULL),
(27, 'NAC-202', 'nacido', '38.00', '2023-11-05', '2023-11-05', 'Angus', 'Hijo de vaca 102', 3, NULL),
(28, 'NAC-203', 'nacido', '32.00', '2023-11-10', '2023-11-10', 'Brangus', 'Parto gemelar A', 3, NULL),
(29, 'NAC-204', 'nacido', '31.00', '2023-11-10', '2023-11-10', 'Brangus', 'Parto gemelar B', 3, NULL),
(30, 'NAC-205', 'nacido', '40.00', '2023-11-15', '2023-11-15', 'Charolais', 'Parto distócico', 3, NULL),
(31, 'ENF-901', 'comprado', '250.00', '2023-07-01', '2023-01-01', 'Cruza', 'Neumonía', 4, 2),
(32, 'ENF-902', 'comprado', '240.00', '2023-07-01', '2023-01-05', 'Cruza', 'Pododermatitis (Gabarro)', 4, 2),
(33, 'ENF-903', 'nacido', '120.00', '2023-05-01', '2023-05-01', 'Angus', 'Herida en pata', 4, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_formula`
--

CREATE TABLE `detalle_formula` (
  `id_formula` int(11) NOT NULL,
  `id_item` int(11) NOT NULL,
  `porcentaje` decimal(5,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `detalle_formula`
--

INSERT INTO `detalle_formula` (`id_formula`, `id_item`, `porcentaje`) VALUES
(1, 1, '50.00'),
(1, 2, '15.00'),
(1, 3, '30.00'),
(1, 5, '5.00'),
(2, 1, '65.00'),
(2, 2, '20.00'),
(2, 4, '10.00'),
(2, 5, '5.00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `formula_alimento`
--

CREATE TABLE `formula_alimento` (
  `id_formula` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `costo_kg` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `formula_alimento`
--

INSERT INTO `formula_alimento` (`id_formula`, `nombre`, `costo_kg`) VALUES
(1, 'Fórmula Crecimiento', '6.50'),
(2, 'Fórmula Engorda', '8.20');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `item`
--

CREATE TABLE `item` (
  `id_item` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo` enum('medicamento','alimento','herramienta') NOT NULL,
  `costo` decimal(10,2) NOT NULL,
  `cantidad` decimal(10,2) DEFAULT '0.00',
  `dias_retiro_carne` int(11) DEFAULT '0',
  `ingrediente_activo` varchar(100) DEFAULT NULL,
  `categoria_sanitaria` enum('NA','Vacuna','Desparasitante','Antibiotico','Vitamina') DEFAULT 'NA',
  `unidad_medida` enum('ml','dosis','gramos','unidad') DEFAULT 'unidad',
  `dias_retiro_leche` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `item`
--

INSERT INTO `item` (`id_item`, `nombre`, `tipo`, `costo`, `cantidad`, `dias_retiro_carne`, `ingrediente_activo`, `categoria_sanitaria`, `unidad_medida`, `dias_retiro_leche`) VALUES
(1, 'Maíz Rolado', 'alimento', '7.50', '15000.00', 0, NULL, 'NA', 'unidad', 0),
(2, 'Pasta de Soya', 'alimento', '11.20', '5000.00', 0, NULL, 'NA', 'unidad', 0),
(3, 'Rastrojo Molido', 'alimento', '2.00', '8000.00', 0, NULL, 'NA', 'unidad', 0),
(4, 'Melaza', 'alimento', '4.50', '1000.00', 0, NULL, 'NA', 'unidad', 0),
(5, 'Núcleo Mineral', 'alimento', '25.00', '500.00', 0, NULL, 'NA', 'unidad', 0),
(6, 'Ivermectina 1%', 'medicamento', '450.00', '20.00', 28, 'Ivermectina', 'NA', 'unidad', 0),
(7, 'Oxitetraciclina', 'medicamento', '380.00', '10.00', 21, 'Oxitetraciclina', 'NA', 'unidad', 0),
(8, 'Implante Zeranol', 'medicamento', '1200.00', '50.00', 0, 'Zeranol', 'NA', 'unidad', 0),
(9, 'Arete Identificador', 'herramienta', '30.00', '100.00', 0, NULL, 'NA', 'unidad', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lote`
--

CREATE TABLE `lote` (
  `id_lote` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `corral` varchar(50) DEFAULT NULL,
  `fecha_inicia` date DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `lote`
--

INSERT INTO `lote` (`id_lote`, `nombre`, `corral`, `fecha_inicia`, `estado`) VALUES
(1, 'Lote 1 - Desarrollo', 'Corral A', '2023-08-01', 'Activo'),
(2, 'Lote 2 - Finalización', 'Corral B', '2023-06-01', 'Activo'),
(3, 'Lote 3 - Maternidad', 'Corral C', '2023-10-01', 'Activo'),
(4, 'Lote 4 - Enfermería', 'Corral Aislamiento', '2023-01-01', 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `id_proveedor` int(11) NOT NULL,
  `rfc` varchar(20) DEFAULT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`id_proveedor`, `rfc`, `nombre`, `telefono`, `direccion`) VALUES
(1, 'GSF900101HA1', 'Ganadera Santa Fe', '555-111-2222', 'Veracruz, VER'),
(2, 'AIN880505BB2', 'Agroinsumos del Norte', '818-333-4444', 'Monterrey, NL'),
(3, 'RES770707CC3', 'Rancho El Semental', '333-555-6666', 'Guadalajara, JAL'),
(4, 'IBO990909DD4', 'Importadora Bovina', '662-777-8888', 'Hermosillo, SON');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_alimento`
--

CREATE TABLE `registro_alimento` (
  `id_registro` int(11) NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `racion_asignada` decimal(10,2) DEFAULT NULL,
  `racion_consumida` decimal(10,2) DEFAULT NULL,
  `comentarios` text,
  `id_animal` int(11) NOT NULL,
  `id_formula_alimento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `registro_alimento`
--

INSERT INTO `registro_alimento` (`id_registro`, `fecha`, `racion_asignada`, `racion_consumida`, `comentarios`, `id_animal`, `id_formula_alimento`) VALUES
(1, '2023-12-01 07:00:00', '14.00', '14.00', NULL, 1, 2),
(2, '2023-12-01 07:00:00', '14.00', '13.50', 'Sobrante leve', 2, 2),
(3, '2023-12-01 07:00:00', '14.50', '14.50', NULL, 3, 2),
(4, '2023-12-01 07:00:00', '14.00', '14.00', NULL, 4, 2),
(5, '2023-12-01 07:00:00', '13.50', '10.00', 'Comió poco', 5, 2),
(6, '2023-12-01 08:00:00', '8.00', '8.00', NULL, 16, 1),
(7, '2023-12-01 08:00:00', '8.00', '8.00', NULL, 17, 1),
(8, '2023-12-01 08:00:00', '8.00', '8.00', NULL, 18, 1),
(9, '2023-12-02 07:00:00', '14.00', '14.00', NULL, 1, 2),
(10, '2023-12-02 07:00:00', '14.00', '14.00', 'Mejor apetito', 2, 2),
(11, '2023-12-02 07:00:00', '14.50', '14.50', NULL, 3, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_peso`
--

CREATE TABLE `registro_peso` (
  `id_registro` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `peso` decimal(10,2) NOT NULL,
  `observaciones` text,
  `id_animal` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `registro_peso`
--

INSERT INTO `registro_peso` (`id_registro`, `fecha`, `peso`, `observaciones`, `id_animal`) VALUES
(1, '2023-06-01', '300.00', 'Ingreso', 1),
(2, '2023-08-01', '360.00', 'Control', 1),
(3, '2023-10-01', '420.00', 'Control', 1),
(4, '2023-12-01', '480.00', 'Pre-Venta', 1),
(5, '2023-06-01', '295.00', 'Ingreso', 2),
(6, '2023-08-01', '350.00', 'Control', 2),
(7, '2023-10-01', '405.00', 'Control', 2),
(8, '2023-12-01', '460.00', 'Pre-Venta', 2),
(9, '2023-06-01', '330.00', 'Ingreso', 10),
(10, '2023-08-01', '390.00', 'Control', 10),
(11, '2023-10-01', '460.00', 'Control', 10),
(12, '2023-12-01', '530.00', 'Listo', 10),
(13, '2023-08-15', '180.00', 'Ingreso', 16),
(14, '2023-10-15', '210.00', 'Control', 16),
(15, '2023-12-01', '235.00', 'Va bien', 16),
(16, '2023-07-01', '250.00', 'Ingreso', 31),
(17, '2023-09-01', '270.00', 'Control', 31),
(18, '2023-11-01', '260.00', 'Bajó por enfermedad', 31);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_sanitario`
--

CREATE TABLE `registro_sanitario` (
  `id_registro` int(11) NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `tipo_evento` varchar(50) DEFAULT NULL,
  `responsable` varchar(100) DEFAULT NULL,
  `dosis` decimal(10,2) DEFAULT NULL,
  `id_item` int(11) NOT NULL,
  `id_animal` int(11) NOT NULL,
  `fecha_proximo_refuerzo` date DEFAULT NULL,
  `sugerencia_proximo_evento` varchar(100) DEFAULT NULL,
  `costo_aplicacion` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `registro_sanitario`
--

INSERT INTO `registro_sanitario` (`id_registro`, `fecha`, `tipo_evento`, `responsable`, `dosis`, `id_item`, `id_animal`, `fecha_proximo_refuerzo`, `sugerencia_proximo_evento`, `costo_aplicacion`) VALUES
(1, '2023-08-02 08:00:00', 'Desparasitación', 'MVZ. Juan', '10.00', 6, 1, NULL, NULL, NULL),
(2, '2023-08-02 08:05:00', 'Desparasitación', 'MVZ. Juan', '10.00', 6, 2, NULL, NULL, NULL),
(3, '2023-08-02 08:10:00', 'Desparasitación', 'MVZ. Juan', '10.00', 6, 3, NULL, NULL, NULL),
(4, '2023-08-02 08:15:00', 'Desparasitación', 'MVZ. Juan', '10.00', 6, 4, NULL, NULL, NULL),
(5, '2023-08-02 08:20:00', 'Desparasitación', 'MVZ. Juan', '10.00', 6, 5, NULL, NULL, NULL),
(6, '2023-06-05 10:00:00', 'Implante', 'MVZ. Juan', '1.00', 8, 1, NULL, NULL, NULL),
(7, '2023-06-05 10:05:00', 'Implante', 'MVZ. Juan', '1.00', 8, 2, NULL, NULL, NULL),
(8, '2023-11-15 09:00:00', 'Antibiótico', 'Caporal', '15.00', 7, 31, NULL, NULL, NULL),
(9, '2023-11-16 09:00:00', 'Antibiótico', 'Caporal', '15.00', 7, 31, NULL, NULL, NULL),
(10, '2023-11-17 09:00:00', 'Antibiótico', 'Caporal', '15.00', 7, 31, NULL, NULL, NULL),
(11, '2023-11-20 10:00:00', 'Curación', 'Caporal', '5.00', 7, 32, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name_surname` varchar(100) NOT NULL,
  `email_user` varchar(50) NOT NULL,
  `pass_user` text NOT NULL,
  `created_user` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name_surname`, `email_user`, `pass_user`, `created_user`) VALUES
(1, 'Urian', 'dev@gmail.com', 'scrypt:32768:8:1$ZXqvqovbXYQZdrAB$66758083429739f4f8985992b22cb89fb58c04b99010858e7fb26f73078a23dd3e16019a17bf881108d582a91a635d2c21d26d80da1612c2d9c9bbb9b06452dc', '2023-07-22 02:10:01'),
(2, 'demo', 'demo@gmail.com', 'scrypt:32768:8:1$Yl2tGU1Ru1Q4Jrzq$d88a0ded538dcfc3a01c8ebf4ea77700576203f6a7cc765f04627464c6047bdcf8eaad84ca3cf0bb5ed058d2dff8ee7a0ba690803538764bedc3ba6173ac6a8a', '2023-07-22 02:29:28'),
(3, 'Omar Emmanuel Lara Juárez', 'olara@utzac.edu.mx', 'scrypt:32768:8:1$pPF8B0lNiGEKRi3A$96c547fa6844bfb6f56d6e907c61e3a7ed691c76d48985fb67ec806dea660134da6add4f0586aa726feded89a28ec9aa460cd451483a31bb3d27a14180727784', '2025-12-02 10:22:58');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `animal`
--
ALTER TABLE `animal`
  ADD PRIMARY KEY (`id_animal`),
  ADD UNIQUE KEY `arete` (`arete`),
  ADD KEY `id_lote` (`id_lote`),
  ADD KEY `id_proveedor` (`id_proveedor`);

--
-- Indices de la tabla `detalle_formula`
--
ALTER TABLE `detalle_formula`
  ADD PRIMARY KEY (`id_formula`,`id_item`),
  ADD KEY `id_item` (`id_item`);

--
-- Indices de la tabla `formula_alimento`
--
ALTER TABLE `formula_alimento`
  ADD PRIMARY KEY (`id_formula`);

--
-- Indices de la tabla `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`id_item`);

--
-- Indices de la tabla `lote`
--
ALTER TABLE `lote`
  ADD PRIMARY KEY (`id_lote`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- Indices de la tabla `registro_alimento`
--
ALTER TABLE `registro_alimento`
  ADD PRIMARY KEY (`id_registro`),
  ADD KEY `id_animal` (`id_animal`),
  ADD KEY `id_formula_alimento` (`id_formula_alimento`);

--
-- Indices de la tabla `registro_peso`
--
ALTER TABLE `registro_peso`
  ADD PRIMARY KEY (`id_registro`),
  ADD KEY `id_animal` (`id_animal`);

--
-- Indices de la tabla `registro_sanitario`
--
ALTER TABLE `registro_sanitario`
  ADD PRIMARY KEY (`id_registro`),
  ADD KEY `id_item` (`id_item`),
  ADD KEY `id_animal` (`id_animal`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `animal`
--
ALTER TABLE `animal`
  MODIFY `id_animal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `formula_alimento`
--
ALTER TABLE `formula_alimento`
  MODIFY `id_formula` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `item`
--
ALTER TABLE `item`
  MODIFY `id_item` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `lote`
--
ALTER TABLE `lote`
  MODIFY `id_lote` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `registro_alimento`
--
ALTER TABLE `registro_alimento`
  MODIFY `id_registro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `registro_peso`
--
ALTER TABLE `registro_peso`
  MODIFY `id_registro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `registro_sanitario`
--
ALTER TABLE `registro_sanitario`
  MODIFY `id_registro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `animal`
--
ALTER TABLE `animal`
  ADD CONSTRAINT `animal_ibfk_1` FOREIGN KEY (`id_lote`) REFERENCES `lote` (`id_lote`),
  ADD CONSTRAINT `animal_ibfk_2` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedor` (`id_proveedor`);

--
-- Filtros para la tabla `detalle_formula`
--
ALTER TABLE `detalle_formula`
  ADD CONSTRAINT `detalle_formula_ibfk_1` FOREIGN KEY (`id_formula`) REFERENCES `formula_alimento` (`id_formula`),
  ADD CONSTRAINT `detalle_formula_ibfk_2` FOREIGN KEY (`id_item`) REFERENCES `item` (`id_item`);

--
-- Filtros para la tabla `registro_alimento`
--
ALTER TABLE `registro_alimento`
  ADD CONSTRAINT `registro_alimento_ibfk_1` FOREIGN KEY (`id_animal`) REFERENCES `animal` (`id_animal`),
  ADD CONSTRAINT `registro_alimento_ibfk_2` FOREIGN KEY (`id_formula_alimento`) REFERENCES `formula_alimento` (`id_formula`);

--
-- Filtros para la tabla `registro_peso`
--
ALTER TABLE `registro_peso`
  ADD CONSTRAINT `registro_peso_ibfk_1` FOREIGN KEY (`id_animal`) REFERENCES `animal` (`id_animal`);

--
-- Filtros para la tabla `registro_sanitario`
--
ALTER TABLE `registro_sanitario`
  ADD CONSTRAINT `registro_sanitario_ibfk_1` FOREIGN KEY (`id_item`) REFERENCES `item` (`id_item`),
  ADD CONSTRAINT `registro_sanitario_ibfk_2` FOREIGN KEY (`id_animal`) REFERENCES `animal` (`id_animal`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

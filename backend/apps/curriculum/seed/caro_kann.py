"""Caro-Kann Defence / Defensa Caro-Kann (B10–B19)."""

from .schema import ExerciseSpec, OpeningSpec, TheorySpec, VariationSpec

CK = ["e4", "c6", "d4", "d5"]
CK_MAIN = CK + ["Nc3", "dxe4", "Nxe4"]

CARO_KANN = OpeningSpec(
    slug="caro-kann",
    name="Defensa Caro-Kann",
    alternative_names=["Caro-Kann Defence"],
    eco_range="B10-B19",
    colour="black",
    first_played="Horatio Caro y Marcus Kann, 1886",
    line=CK,
    tagline="Disputar el centro con ...c6 y ...d5 sin encerrar ni una pieza.",
    summary=(
        "Las negras preparan ...d5 con el peón de c en lugar del de e, así que el alfil de "
        "c8 sale antes de que se cierre la diagonal. Menos ambiciosa que la Siciliana y "
        "mucho más difícil de romper."
    ),
    description="""
La Caro-Kann resuelve el problema de la Defensa Francesa antes de que aparezca. Las dos
preparan ...d5, pero la Francesa lo hace con ...e6 y deja el alfil de c8 encerrado detrás
de su propia cadena de peones durante media partida. La Caro-Kann lo hace con **...c6**,
y el alfil sale a f5 o g4 con total comodidad.

El precio es un tiempo: el peón de c ocupa la casilla natural del caballo de b8 y las
negras tardan más en generar contrajuego. A cambio consiguen algo poco habitual contra
1.e4: **una posición sin ninguna debilidad estructural**.

## Las cuatro maneras de enfrentarla

Las blancas eligen pronto y cada elección lleva a un tipo de partida distinto:

- **3.Cc3 / 3.Cd2** (Clásica y variantes con ...Cd7): las blancas dejan que las negras
  cambien en e4 y juegan a tener más espacio y mejor desarrollo. Es la línea principal.
- **3.e5** (Avance): cierra el centro y gana espacio. Aquí sí que las negras tienen que
  sacar el alfil a f5 de inmediato, antes de que la casilla se cierre.
- **3.exd5 cxd5 4.c4** (Panov-Botvinnik): las blancas cambian de género y juegan una
  posición de peón dama aislado, con piezas activas y juego rápido.
- **3.f3** (Fantasía) y **2.Cc3** (Dos Caballos): intentos de sacar a las negras del guion
  desde la jugada 2 o 3.

## Reputación

La Caro-Kann tiene fama de aburrida y es un malentendido. Es **sólida**, que no es lo
mismo: Botvinnik, Petrosian, Karpov y Anand la usaron en campeonatos del mundo, y las
líneas del Avance y del Panov producen partidas tan agudas como cualquier Siciliana. Lo
que no da es contrajuego automático: hay que ganárselo.
""".strip(),
    variations=[
        VariationSpec(
            slug="caro-kann-clasica",
            name="Variante Clásica",
            eco="B18-B19",
            line=CK_MAIN
            + [
                "Bf5", "Ng3", "Bg6", "h4", "h6", "Nf3", "Nd7", "h5", "Bh7",
                "Bd3", "Bxd3", "Qxd3", "e6", "Bf4", "Ngf6", "O-O-O", "Be7",
            ],
            tagline="4...Af5: sacar el alfil bueno antes de cerrar nada. Ésa es toda la apertura.",
            is_main_line=True,
            difficulty=3,
            drill_plies=[7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            drill_difficulty=3,
            idea=(
                "Las negras cambian su alfil bueno por el blanco de d3 y se quedan con una "
                "estructura sin debilidades. Las blancas enrocan largo y atacan con los peones."
            ),
            description="""
**4...Af5** es la jugada que justifica toda la Caro-Kann. El alfil sale a su mejor casilla
antes de que ...e6 lo encierre, y ataca de paso el caballo de e4.

Lo que sigue es una de las secuencias más largas y más memorizables de la teoría moderna:
**5.Cg3 Ag6 6.h4 h6 7.Cf3 Cd7 8.h5 Ah7 9.Ad3 Axd3 10.Dxd3**. Las blancas ganan espacio en
el flanco de rey con los peones de h, y acaban cambiando el alfil que a las negras les
costó tanto sacar. No es una contradicción: el cambio le cuesta a las blancas varios
tiempos y las negras se quedan con una estructura que no tiene por dónde atacarse.

La posición tras **12.O-O-O** define la partida: enroques opuestos, blancas con más espacio
y ataque de peones, negras con una fortaleza sin grietas y la ruptura ...c5 en el bolsillo.
""".strip(),
            theory=[
                TheorySpec(
                    title="Por qué las negras permiten 8.h5",
                    kind="idea",
                    body=(
                        "Cuesta aceptar que las negras dejen encerrar el alfil en h7. La razón "
                        "es aritmética: h4 y h5 son dos jugadas de peón que no desarrollan nada "
                        "y que debilitan g5 y g4 para el final. Las negras entregan la "
                        "comodidad del alfil a cambio de tiempo y de una estructura que "
                        "aguanta cualquier ataque."
                    ),
                    line=CK_MAIN + ["Bf5", "Ng3", "Bg6", "h4", "h6", "Nf3", "Nd7", "h5", "Bh7"],
                    highlight=["h5", "h7", "g5"],
                    orientation="black",
                ),
                TheorySpec(
                    title="La ruptura ...c5 es el plan, no una opción",
                    kind="plan",
                    body=(
                        "Con las blancas enrocadas largo, las negras atacan por donde está el "
                        "rey: la columna c. **...c5** abre esa columna y le da sentido a la "
                        "torre de c8 y al caballo de d7. Sin ...c5 las negras están sólidas y "
                        "no tienen nada; con ...c5 la posición es una partida de verdad."
                    ),
                    highlight=["c5", "c1", "c8"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="caro-kann-karpov",
            name="Variante Karpov",
            eco="B17",
            line=CK_MAIN
            + ["Nd7", "Ng5", "Ngf6", "Bd3", "e6", "N1f3", "Bd6", "Qe2", "h6", "Ne4", "Nxe4", "Qxe4"],
            tagline="4...Cd7: preparar ...Cgf6 sin que el cambio en f6 estropee la estructura.",
            difficulty=4,
            drill_plies=[7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            drill_difficulty=4,
            idea=(
                "El caballo de d7 recaptura en f6, así que las negras pueden desarrollar el "
                "otro caballo sin quedarse con peones doblados."
            ),
            description="""
También llamada Variante Smyslov. **4...Cd7** parece pasiva y es profundamente práctica:
prepara ...Cgf6 de modo que, si las blancas cambian en f6, recaptura el caballo de d7 y la
estructura negra sigue intacta. Compárala con la Bronstein-Larsen o la Tartakower, donde
la recaptura la hace un peón y la estructura cambia para siempre.

Karpov la jugó durante décadas con una idea muy suya: no pasa nada por estar ligeramente
peor si no hay ninguna debilidad que atacar.

**Cuidado con el orden de jugadas.** Esta variante contiene la celada más famosa de toda
la Caro-Kann, y cae en ella todo el mundo una vez.
""".strip(),
            exercises=[
                ExerciseSpec(
                    ref="caro-kann-karpov-mate-relampago",
                    prompt=(
                        "Las negras acaban de jugar 5...Cgf6, que parece la jugada más natural "
                        "del mundo. Castígalo: hay mate en una."
                    ),
                    setup=CK_MAIN + ["Nd7", "Qe2", "Ngf6"],
                    answer=["Nd6#"],
                    kind="trap",
                    difficulty=2,
                    expect="mate",
                    themes=["mate", "clavada", "celada"],
                    hint="La dama de e2 ya está haciendo un trabajo. ¿Qué casilla no puede usar el rey?",
                    explanation=(
                        "**6.Cd6** es mate ahogado en toda regla. El peón de e7 no puede capturar "
                        "porque está clavado por la dama de e2 contra el rey, el peón de c está "
                        "en c6 y no llega a d6, y el rey no tiene ni una casilla: d7 lo ocupa su "
                        "propio caballo, f8 su alfil, d8 su dama. Por esto las negras juegan "
                        "**5...Cdf6** o **5...Cb6** cuando la dama blanca aparece en e2."
                    ),
                ),
            ],
            theory=[
                TheorySpec(
                    title="La regla que evita el desastre",
                    kind="warning",
                    body=(
                        "En cuanto la dama blanca llegue a e2 con el caballo en e4 y el caballo "
                        "negro en d7, **la casilla d6 es mate**. Antes de jugar ...Cgf6, mira la "
                        "columna e. Es una comprobación de dos segundos que ahorra partidas "
                        "enteras."
                    ),
                    line=CK_MAIN + ["Nd7", "Qe2"],
                    highlight=["d6", "e2", "e7", "e8"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="caro-kann-avance",
            name="Variante del Avance",
            eco="B12",
            line=CK + ["e5", "Bf5", "Nf3", "e6", "Be2", "c5", "Be3", "Nd7"],
            tagline="3.e5: cerrar el centro y ganar espacio. Las negras tienen una jugada para reaccionar.",
            is_main_line=True,
            difficulty=3,
            drill_plies=[4, 5, 6, 7, 8, 9, 10, 11],
            drill_difficulty=2,
            idea=(
                "Las blancas ganan espacio; las negras sacan el alfil a f5 antes de jugar "
                "...e6 y luego minan la cadena de peones con ...c5."
            ),
            description="""
**3.e5** es la respuesta más popular hoy, y también la más lógica: si la Caro-Kann existe
para sacar el alfil de c8, cerremos el centro y veamos si le da tiempo.

Le da tiempo, justo: **3...Af5** es prácticamente obligado. Después de eso las negras
juegan ...e6 con la conciencia tranquila y atacan la base de la cadena blanca con **...c5**.

La versión moderna con **4.Cf3 e6 5.Ae2** se llama Variante Short, y la idea es sutil: en
lugar de perseguir el alfil negro con 4.h4 o 4.Cc3, las blancas se desarrollan y juegan
c2-c4 o Ae3 y Cbd2 para sostener d4. Espacio contra solidez, otra vez.

El error que hay que no cometer aquí está en la jugada 3, y lo comete todo el que viene de
jugar la Francesa.
""".strip(),
            theory=[
                TheorySpec(
                    title="Cadena de peones: se ataca por la base",
                    kind="structure",
                    body=(
                        "La cadena blanca es d4-e5. Su base es **d4**, y por eso las negras "
                        "juegan ...c5 y no ...f6. Atacar la punta con ...f6 abre líneas hacia "
                        "el propio rey; atacar la base con ...c5 obliga a las blancas a decidir "
                        "entre cambiar (y perder espacio) o defender (y quedarse quietas)."
                    ),
                    line=CK + ["e5", "Bf5", "Nf3", "e6", "Be2", "c5"],
                    highlight=["d4", "e5", "c5"],
                    orientation="black",
                ),
            ],
            exercises=[
                ExerciseSpec(
                    ref="caro-kann-avance-alfil-fuera",
                    prompt=(
                        "Las blancas han jugado 3.e5. Hay una jugada que hay que hacer ahora o "
                        "no se podrá hacer nunca. ¿Cuál es?"
                    ),
                    setup=CK + ["e5"],
                    answer=["Bf5"],
                    kind="plan",
                    difficulty=1,
                    themes=["desarrollo", "alfil malo", "estructura"],
                    hint="¿Qué pieza se quedaría encerrada si jugaras ...e6 primero?",
                    explanation=(
                        "**3...Af5** es la razón de ser de la Caro-Kann. Si las negras juegan "
                        "3...e6 primero, el alfil de c8 queda encerrado detrás de sus propios "
                        "peones y la posición se convierte en una Defensa Francesa con el peón "
                        "en c6 en lugar de en c7: una Francesa mala, con un tiempo perdido. "
                        "Todo lo que hace esta apertura distinta pasa por esta jugada."
                    ),
                ),
            ],
        ),
        VariationSpec(
            slug="caro-kann-panov",
            name="Ataque Panov-Botvinnik",
            eco="B13-B14",
            line=CK
            + ["exd5", "cxd5", "c4", "Nf6", "Nc3", "e6", "Nf3", "Be7", "cxd5", "Nxd5", "Bd3", "Nc6", "O-O", "O-O"],
            tagline="4.c4: convertir la Caro-Kann en una partida de peón dama aislado.",
            difficulty=4,
            drill_plies=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            drill_difficulty=3,
            idea=(
                "Las blancas aceptan un peón aislado en d4 a cambio de piezas activas, la "
                "casilla e5 y ataque al rey. Las negras juegan a llegar al final."
            ),
            description="""
El Panov cambia el género de la partida. Con **3.exd5 cxd5 4.c4** las blancas se apuntan a
una estructura de **peón dama aislado**, que es una de las posiciones más instructivas del
ajedrez.

El trato es siempre el mismo:

- **El bando con el peón aislado** (las blancas) tiene más espacio, la casilla **e5** para
  el caballo, columnas semiabiertas y piezas activas. Quiere atacar en el medio juego.
- **El bando que juega contra él** (las negras) quiere **cambiar piezas**. Cada cambio
  acerca el final, y en el final el peón de d4 es sólo una debilidad que hay que defender.

Esa tensión —atacar antes de que se cambien las piezas— es toda la partida. El Panov no es
teoría de memoria, es entender bien una estructura.
""".strip(),
            theory=[
                TheorySpec(
                    title="El bloqueo de d5",
                    kind="structure",
                    body=(
                        "La casilla **d5**, delante del peón aislado, es el mejor sitio del "
                        "tablero para una pieza negra: no puede ser expulsada por ningún peón. "
                        "Poner un caballo ahí y cambiar damas es el plan negro completo. Las "
                        "blancas, a su vez, luchan por **e5** por la misma razón."
                    ),
                    highlight=["d4", "d5", "e5"],
                ),
                TheorySpec(
                    title="Cambiar piezas es una jugada de ataque",
                    kind="plan",
                    body=(
                        "Contra un peón aislado, ofrecer cambios no es pasivo: es el plan. Cada "
                        "pareja de piezas que desaparece reduce el potencial de ataque blanco y "
                        "deja el peón de d4 más solo. Es de los pocos sitios del ajedrez donde "
                        "simplificar y jugar a ganar son la misma cosa."
                    ),
                    highlight=["d4"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="caro-kann-cambio",
            name="Variante del Cambio",
            eco="B13",
            line=CK + ["exd5", "cxd5", "Bd3", "Nc6", "c3", "Nf6", "Bf4", "Bg4", "Qb3", "Qd7"],
            tagline="4.Ad3: estructura simétrica y un plan lento de minoría.",
            difficulty=2,
            drill_plies=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            drill_difficulty=2,
            idea=(
                "Posición simétrica donde las blancas juegan con un tiempo de más y preparan "
                "el ataque de minorías con b4-b5."
            ),
            description="""
**3.exd5 cxd5 4.Ad3** deja una posición casi simétrica. No promete ventaja y no busca
complicaciones: las blancas juegan a tener un tiempo de más y a un plan muy concreto, el
**ataque de minorías**.

La idea: las blancas avanzan **b2-b4-b5** en el flanco donde tienen menos peones. Cuando
b5 captura en c6, las negras se quedan con un peón débil y aislado en una columna abierta,
y ese peón es el objetivo del resto de la partida.

Es una variante excelente para aprender a jugar posiciones tranquilas: aquí no hay
tácticas que valgan, sólo un plan ejecutado durante treinta jugadas.
""".strip(),
            theory=[
                TheorySpec(
                    title="Atacar con menos peones",
                    kind="plan",
                    body=(
                        "El ataque de minorías es contraintuitivo: se avanza en el flanco donde "
                        "se tienen **menos** peones. El objetivo no es ganar espacio ni crear un "
                        "pasado, sino forzar un cambio que deje al rival con un peón débil y "
                        "permanente. Si b5xc6 obliga a ...bxc6, ese peón de c6 será el objetivo "
                        "hasta el final de la partida."
                    ),
                    highlight=["b4", "b5", "c6"],
                ),
            ],
        ),
        VariationSpec(
            slug="caro-kann-fantasia",
            name="Variante Fantasía",
            eco="B12",
            line=CK + ["f3", "dxe4", "fxe4", "e5", "Nf3", "exd4", "Bc4", "Nf6", "O-O"],
            tagline="3.f3: sostener e4 con un peón y jugar a atacar desde la jugada 3.",
            difficulty=4,
            drill_plies=[4, 5, 6, 7, 8, 9, 10, 11, 12],
            drill_difficulty=4,
            idea=(
                "Las blancas construyen un centro grande a costa de la seguridad de su rey. "
                "Es un gambito de desarrollo disfrazado de jugada sólida."
            ),
            description="""
**3.f3** parece una jugada de principiante y es una de las armas más incómodas contra la
Caro-Kann. Las blancas defienden e4 con un peón para poder recapturar con otro peón y
quedarse con un centro de d4+e4 macizo.

El coste es serio: la diagonal e1-h4 queda abierta y el rey blanco se queda sin la casilla
f2 defendida. La línea **3...dxe4 4.fxe4 e5 5.Cf3 exd4 6.Ac4** es un gambito puro: las
blancas entregan el peón de d4 por desarrollo y ataque contra f7.

Es una variante para jugadores que prefieren llevar al rival a un terreno sin caminos
marcados. Y para las negras es un aviso: aquí no vale desarrollarse de memoria.
""".strip(),
        ),
        VariationSpec(
            slug="caro-kann-dos-caballos",
            name="Variante de los Dos Caballos",
            eco="B11",
            line=["e4", "c6", "Nc3", "d5", "Nf3", "Bg4", "h3", "Bxf3", "Qxf3", "e6", "d3", "Nf6"],
            tagline="2.Cc3 y 3.Cf3: desarrollar los dos caballos antes de tocar el centro.",
            difficulty=3,
            drill_plies=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            drill_difficulty=3,
            idea=(
                "Las blancas evitan toda la teoría de 2.d4 y juegan una partida de piezas. "
                "Las negras suelen cambiar en f3 para no quedarse con el alfil sin casillas."
            ),
            description="""
**2.Cc3 d5 3.Cf3** se salta de un plumazo la Clásica, el Avance y el Panov. Las blancas
desarrollan y dejan el peón de d en casa, listo para d3 o d4 según convenga.

La respuesta más natural es **3...Ag4**, clavando el caballo antes de que h3 se lo impida.
Tras **4.h3 Axf3 5.Dxf3** las blancas se quedan con la pareja de alfiles y una dama activa;
las negras, con una estructura sana y sin problemas de desarrollo.

Es una variante de estilo: quien la juega busca una partida de comprensión, no de
preparación.
""".strip(),
        ),
        VariationSpec(
            slug="caro-kann-bronstein-larsen",
            name="Variante Bronstein-Larsen",
            eco="B16",
            line=CK_MAIN + ["Nf6", "Nxf6+", "gxf6", "Nf3", "Bg4", "Be2", "e6"],
            tagline="5...gxf6: romper la propia estructura a propósito, a cambio de líneas abiertas.",
            difficulty=4,
            drill_plies=[7, 8, 9, 10, 11, 12, 13],
            drill_difficulty=4,
            idea=(
                "Las negras aceptan peones doblados en f para abrir la columna g y quedarse "
                "con un centro de peones móvil y dos alfiles."
            ),
            description="""
**5...gxf6** va contra todo lo que enseña un manual, y por eso es interesante. Las negras
se quedan con peones doblados y un enroque corto imposible.

A cambio consiguen tres cosas concretas: la **columna g abierta** apuntando al enroque
blanco, un **centro de peones** (e6, f6, f7) capaz de avanzar con ...e5, y la pareja de
alfiles con líneas para moverse. Suelen enrocar largo y jugar a atacar.

Larsen la usó porque odiaba las tablas. Es una elección de temperamento: la Caro-Kann más
desequilibrada que existe, dentro de la apertura con más fama de tranquila.
""".strip(),
        ),
        VariationSpec(
            slug="caro-kann-tartakower",
            name="Variante Tartakower",
            eco="B15",
            line=CK_MAIN + ["Nf6", "Nxf6+", "exf6", "Bc4", "Bd6", "Qe2+", "Qe7", "Qxe7+", "Kxe7"],
            tagline="5...exf6: recapturar hacia el centro y aceptar un final ligeramente peor.",
            difficulty=3,
            drill_plies=[7, 8, 9, 10, 11, 12, 13, 14, 15],
            drill_difficulty=3,
            idea=(
                "La recaptura sensata: estructura sólida, desarrollo rápido y un final donde "
                "la mayoría blanca del flanco de dama es la única ventaja real."
            ),
            description="""
La hermana prudente de la Bronstein-Larsen. **5...exf6** deja los peones doblados en f pero
mantiene una estructura razonable y abre la diagonal del alfil de f8, que sale a d6 de
inmediato.

Las negras aceptan que las blancas tienen una mayoría de peones sana en el flanco de dama
(3 contra 2) mientras que la mayoría negra del flanco de rey está doblada y no produce
peón pasado. Es la misma aritmética que en la Española del Cambio, con los colores
invertidos.

A cambio, las negras están completamente desarrolladas en cinco jugadas más y no tienen
ninguna casilla débil. Muchos finales de esta variante acaban en tablas, y ése es
exactamente el objetivo de quien la elige.
""".strip(),
            theory=[
                TheorySpec(
                    title="La aritmética de las mayorías",
                    kind="structure",
                    body=(
                        "Flanco de dama: 3 peones blancos contra 2 negros, sanos, capaces de "
                        "crear un pasado. Flanco de rey: 4 negros contra 3 blancos, pero con los "
                        "de f doblados, así que no producen nada. Ésa es la ventaja blanca "
                        "entera, y es pequeña: suficiente para jugar sin riesgo, insuficiente "
                        "para ganar contra una defensa correcta."
                    ),
                    line=CK_MAIN + ["Nf6", "Nxf6+", "exf6"],
                    highlight=["f6", "f7", "a2", "b2", "c2"],
                ),
            ],
        ),
    ],
)

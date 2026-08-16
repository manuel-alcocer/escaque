"""Ruy Lopez / Apertura Española (C60–C99)."""

from .schema import ExerciseSpec, OpeningSpec, TheorySpec, VariationSpec

RUY = ["e4", "e5", "Nf3", "Nc6", "Bb5"]

SPANISH = OpeningSpec(
    slug="apertura-espanola",
    name="Apertura Española",
    alternative_names=["Ruy López"],
    eco_range="C60-C99",
    colour="white",
    first_played="Ruy López de Segura, 1561",
    line=RUY,
    tagline="La presión que no se afloja: 3.Ab5 pregunta por el caballo de c6 y nunca deja de preguntar.",
    summary=(
        "Con 3.Ab5 las blancas atacan al defensor del peón de e5 y ganan tiempo para "
        "enrocar. No hay ganancia material inmediata, y ahí está la gracia: la Española "
        "es una apertura de presión sostenida, no de golpe rápido."
    ),
    description="""
La Española nace de una idea sencilla y termina en el cuerpo teórico más extenso del
ajedrez. Tras **1.e4 e5 2.Cf3 Cc6 3.Ab5**, el alfil no amenaza nada concreto: 4.Axc6
dxc6 5.Cxe5 se refuta con 5...Dd4, que recupera la pieza. Lo que hace 3.Ab5 es fijar
una pregunta permanente sobre el caballo de c6, el defensor del centro negro.

De esa pregunta salen tres respuestas, y las tres son escuelas distintas:

- **3...a6**, la Defensa Morphy, expulsa al alfil antes de decidir nada. Es la puerta
  a la Variante Cerrada, la más jugada de todas.
- **3...Cf6**, la Berlinesa, ignora el flanco de dama y va directa a por e4. Kramnik
  la devolvió a la primera línea en el año 2000 y desde entonces no se ha ido.
- **3...Ac5**, **3...d6** y **3...f5** son terceras vías: la Clásica, la Steinitz y la
  Schliemann, cada una con su propio precio a pagar.

## Lo que hay que entender antes que las jugadas

En la Española casi nadie captura en c6 pronto, porque el cambio entrega la pareja de
alfiles a cambio de una estructura que las negras pueden reparar. El plan blanco típico
es lento y muy reconocible: **c3 y d4** para montar el centro, **Cbd2-f1-g3** para llevar
el caballo de dama al flanco de rey, y **h3** para dejar sitio al alfil de c1 sin permitir
...Ag4. Es la famosa maniobra de tres jugadas que da su nombre a media apertura.

Las negras, mientras tanto, deciden qué hacer con el caballo de c6, que estorba a su
propio peón de c. Casi todos los grandes sistemas negros son respuestas a esa incomodidad:
Chigorin lo lleva a a5, Breyer lo devuelve a b8, Zaitsev lo deja quieto y desarrolla el
alfil a b7.
""".strip(),
    variations=[
        VariationSpec(
            slug="espanola-morphy",
            name="Defensa Morphy",
            eco="C70",
            line=RUY + ["a6", "Ba4", "Nf6", "O-O"],
            tagline="3...a6: preguntar al alfil antes de comprometer nada.",
            is_main_line=True,
            difficulty=1,
            drill_plies=[4, 5, 6, 7, 8],
            drill_difficulty=1,
            idea=(
                "Las negras ganan la opción de expulsar el alfil con ...b5 más adelante. "
                "A cambio, el peón de a6 deja un hueco en b6 y la casilla b5 queda para "
                "siempre en la agenda blanca."
            ),
            description="""
**3...a6** es la jugada más natural del repertorio negro y también la más profunda. No
gana nada de inmediato: 4.Aa4 mantiene la clavada y las blancas siguen igual de cómodas.
Lo que gana es **una amenaza en reserva**. En cualquier momento del futuro, ...b5 expulsa
el alfil a b3, y esa posibilidad condiciona todo lo que las blancas pueden permitirse.

Después de **4.Aa4 Cf6 5.O-O**, las blancas ofrecen el peón de e4. Aceptarlo lleva a la
Defensa Abierta; declinarlo con 5...Ae7 lleva a la Cerrada. La partida se bifurca aquí y
el resto de la Española cuelga de esa decisión.
""".strip(),
            theory=[
                TheorySpec(
                    title="Por qué 4.Axc6 no gana el peón",
                    kind="warning",
                    body=(
                        "La tentación es 4.Axc6 dxc6 5.Cxe5, con un peón de más. Pero "
                        "**5...Dd4** ataca el caballo de e5 y el peón de e4 a la vez, y las "
                        "negras recuperan el material con mejor desarrollo. El peón de e5 "
                        "está defendido de forma indirecta, y esa es la primera lección de "
                        "la apertura."
                    ),
                    line=RUY + ["a6", "Bxc6", "dxc6", "Nxe5", "Qd4"],
                    highlight=["d4", "e5", "e4"],
                    orientation="black",
                ),
                TheorySpec(
                    title="El plan blanco de siempre",
                    kind="plan",
                    body=(
                        "Recuérdalo como una sola unidad: **c3, d4, Cbd2-f1-g3, h3**. Las "
                        "blancas construyen el centro con peones, llevan el caballo de b1 "
                        "al flanco de rey por la ruta larga y sólo entonces atacan. Es lenta "
                        "a propósito: la Española no tiene prisa porque las negras no tienen "
                        "ruptura rápida."
                    ),
                    line=RUY + ["a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3"],
                    highlight=["c3", "d4", "f1", "g3"],
                ),
            ],
            exercises=[
                ExerciseSpec(
                    ref="espanola-morphy-recupera",
                    prompt="Las blancas han jugado 5.Cxe5 y creen que ganan un peón. Refútalo.",
                    setup=RUY + ["a6", "Bxc6", "dxc6", "Nxe5"],
                    answer=["Qd4"],
                    kind="trap",
                    difficulty=2,
                    themes=["doble ataque", "recuperar material"],
                    hint="Busca una jugada que ataque dos piezas a la vez.",
                    explanation=(
                        "**5...Dd4** ataca el caballo de e5 y el peón de e4 simultáneamente. "
                        "Tras 6.Cf3 Dxe4+ las negras recuperan el peón con ventaja de desarrollo, "
                        "y 6.Cd3 Dxe4+ 7.De2 les da un final cómodo con la pareja de alfiles."
                    ),
                ),
            ],
        ),
        VariationSpec(
            slug="espanola-cerrada",
            name="Variante Cerrada",
            eco="C84-C99",
            line=RUY
            + ["a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3", "O-O", "h3"],
            tagline="La posición más jugada de la historia del ajedrez de torneo.",
            is_main_line=True,
            difficulty=2,
            drill_plies=[6, 7, 8, 10, 12, 14, 15, 16],
            drill_difficulty=2,
            idea=(
                "Las negras cierran el centro con ...d6 y aguantan; las blancas montan "
                "c3-d4 y maniobran. Gana quien entienda mejor cuándo abrir."
            ),
            description="""
La posición tras **9.h3** es probablemente la más analizada del ajedrez. Todo está
desarrollado, nadie ha capturado nada y ambos bandos tienen que decidir un plan de
verdad en vez de seguir jugadas naturales.

**Por qué 9.h3 y no 9.d4 inmediatamente:** tras 9.d4 Ag4 las negras clavan el caballo de
f3 justo cuando el centro se abre, y la presión sobre d4 se vuelve incómoda. 9.h3 le
quita esa casilla al alfil antes de tocar el centro. Es una jugada de profilaxis pura, y
explica por qué la Española tiene fama de apertura de paciencia.

Las negras eligen ahora dónde poner el caballo de c6, que está mal colocado a largo plazo
porque bloquea la ruptura ...c5:

- **9...Ca5** (Chigorin) lo lleva al borde para preparar ...c5 de inmediato.
- **9...Cb8** (Breyer) lo devuelve a casa para reubicarlo por d7. Parece absurdo y es una
  de las ideas más profundas de la apertura.
- **9...Ab7** (Zaitsev) lo deja donde está y apunta al centro por la diagonal larga.
""".strip(),
            theory=[
                TheorySpec(
                    title="El problema del caballo de c6",
                    kind="structure",
                    body=(
                        "En casi todas las estructuras españolas las negras quieren jugar "
                        "**...c5**, para atacar d4 y darle aire a la dama. El caballo de c6 "
                        "lo impide. Las tres grandes variantes cerradas (Chigorin, Breyer y "
                        "Zaitsev) son tres soluciones distintas al mismo problema, y elegir "
                        "una es elegir a qué estás dispuesto a renunciar."
                    ),
                    line=RUY
                    + ["a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3", "O-O", "h3"],
                    highlight=["c6", "c5", "d4"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="espanola-chigorin",
            name="Variante Chigorin",
            eco="C96-C99",
            parent="espanola-cerrada",
            line=RUY
            + [
                "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3",
                "O-O", "h3", "Na5", "Bc2", "c5", "d4", "Qc7",
            ],
            tagline="9...Ca5: el caballo al borde para liberar el peón de c.",
            difficulty=3,
            drill_plies=[16, 17, 18, 19, 20, 21],
            drill_difficulty=3,
            idea=(
                "Las negras cambian la calidad del caballo por actividad de peones: ...c5 "
                "presiona d4 y la dama en c7 apoya toda la columna."
            ),
            description="""
**9...Ca5 10.Ac2 c5 11.d4 Dc7** es la interpretación clásica. Las negras aceptan que el
caballo de a5 está feo, porque a cambio consiguen la tensión central que necesitan.

El precio real no es el caballo, es el alfil blanco. Tras 10.Ac2 el alfil apunta a h7 por
la diagonal b1-h7, y muchos ataques blancos en esta línea acaban con **Cf1-g3, Cf5 y
Dd3**, todos apuntando al mismo sitio. La Chigorin es una carrera: presión negra en el
centro contra ataque blanco al rey.
""".strip(),
            theory=[
                TheorySpec(
                    title="La batería que se cocina a fuego lento",
                    kind="plan",
                    body=(
                        "El alfil de c2 y la dama en d3 forman la batería que da sentido al "
                        "ataque blanco. Antes de montarla, las blancas suelen jugar Cbd2-f1-g3 "
                        "para tener una pieza más cerca del rey negro. Si las negras no "
                        "reaccionan en el centro a tiempo, el ataque llega solo."
                    ),
                    highlight=["c2", "d3", "h7"],
                ),
            ],
        ),
        VariationSpec(
            slug="espanola-breyer",
            name="Variante Breyer",
            eco="C94-C95",
            parent="espanola-cerrada",
            line=RUY
            + [
                "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3",
                "O-O", "h3", "Nb8", "d4", "Nbd7",
            ],
            tagline="9...Cb8: devolver el caballo a casa para colocarlo mejor.",
            difficulty=4,
            drill_plies=[16, 17, 18, 19],
            drill_difficulty=3,
            idea=(
                "El caballo va a d7, donde no estorba a ...c5, apoya e5 y deja libre la "
                "diagonal larga para el alfil de b7."
            ),
            description="""
La jugada favorita de Spassky y una de las ideas más contraintuitivas del ajedrez
posicional. **9...Cb8** retrocede voluntariamente para reubicar el caballo en d7, donde
hace tres cosas que no hacía en c6: apoya el peón de e5, no bloquea el peón de c y deja
la diagonal a8-h1 libre para ...Ab7.

Cuesta dos tiempos. En una posición cerrada, dos tiempos se pagan sin drama; lo que no se
paga es tener una pieza mal colocada durante cuarenta jugadas.
""".strip(),
            theory=[
                TheorySpec(
                    title="Cuándo se puede perder tiempo",
                    kind="idea",
                    body=(
                        "La regla de que no se mueve dos veces la misma pieza en la apertura "
                        "vale mientras el centro pueda abrirse de golpe. Aquí no puede: las "
                        "cadenas de peones están trabadas y ninguna ruptura es inmediata. "
                        "En ese contexto, la calidad de la casilla vale más que el tiempo."
                    ),
                    highlight=["b8", "d7", "b7"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="espanola-zaitsev",
            name="Variante Zaitsev",
            eco="C92-C93",
            parent="espanola-cerrada",
            line=RUY
            + [
                "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3",
                "O-O", "h3", "Bb7", "d4", "Re8",
            ],
            tagline="9...Ab7 y 10...Te8: presión directa sobre e4.",
            difficulty=4,
            drill_plies=[16, 17, 18, 19],
            drill_difficulty=3,
            idea=(
                "El alfil de b7 y la torre de e8 apuntan al peón de e4 desde dos direcciones. "
                "Karpov la usó durante veinte años."
            ),
            description="""
La Zaitsev es la variante de la eficiencia: ninguna pieza retrocede, todo apunta al
centro. **9...Ab7** ocupa la diagonal larga y **10...Te8** dobla la presión sobre e4.

Tiene una peculiaridad práctica famosa: las blancas pueden repetir con **11.Cg5 Tf8
12.Cf3 Te8**, ofreciendo tablas por repetición. Quien elige la Zaitsev con negras tiene
que llevar preparada una alternativa si necesita ganar.
""".strip(),
        ),
        VariationSpec(
            slug="espanola-abierta",
            name="Defensa Abierta",
            eco="C80-C83",
            line=RUY + ["a6", "Ba4", "Nf6", "O-O", "Nxe4", "d4", "b5", "Bb3", "d5", "dxe5", "Be6"],
            tagline="5...Cxe4: aceptar el peón y aguantar el tirón.",
            difficulty=3,
            drill_plies=[9, 10, 11, 12, 13, 14, 15],
            drill_difficulty=3,
            idea=(
                "Las negras cogen el peón de e4 y devuelven la iniciativa. El caballo "
                "avanzado se sostiene con ...d5, y el juego se vuelve concreto de inmediato."
            ),
            description="""
**5...Cxe4** cambia el carácter de la partida en una jugada. Ya no hay maniobras lentas:
las negras tienen un caballo en el centro que hay que sostener y las blancas tienen que
demostrar que el desarrollo vale más que el peón.

La secuencia **6.d4 b5 7.Ab3 d5 8.dxe5 Ae6** es el esqueleto de toda la variante. Fíjate
en lo que ha pasado: las negras tienen un peón pasado potencial en d5 y una cuña sólida,
pero su caballo de e4 está pinchado y el peón de e5 blanco corta el tablero en dos.
""".strip(),
            theory=[
                TheorySpec(
                    title="El caballo de e4 no vive solo",
                    kind="warning",
                    body=(
                        "Sin **...d5** el caballo de e4 se cae en dos jugadas (Te1, Cbd2 o "
                        "simplemente d5 expulsando al caballo de c6). Toda la Defensa Abierta "
                        "depende de conseguir ...d5 a tiempo: si no llega, las negras están "
                        "un peón abajo y sin compensación."
                    ),
                    line=RUY + ["a6", "Ba4", "Nf6", "O-O", "Nxe4", "d4", "b5", "Bb3", "d5"],
                    highlight=["e4", "d5"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="espanola-marshall",
            name="Ataque Marshall",
            eco="C89",
            line=RUY
            + [
                "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "O-O", "c3",
                "d5", "exd5", "Nxd5", "Nxe5", "Nxe5", "Rxe5", "c6", "d4", "Bd6",
                "Re1", "Qh4", "g3", "Qh3",
            ],
            tagline="8...d5: un peón por un ataque que dura cuarenta jugadas.",
            difficulty=5,
            drill_plies=[15, 17, 19, 21, 23, 25, 27],
            drill_difficulty=4,
            idea=(
                "Las negras entregan el peón de e5 para abrir líneas contra el rey blanco. "
                "La compensación es posicional y permanente, no una combinación concreta."
            ),
            description="""
Marshall guardó esta idea durante años para soltársela a Capablanca en 1918. Perdió
aquella partida, y aun así el gambito lleva su nombre porque la idea era correcta.

**8...d5 9.exd5 Cxd5 10.Cxe5 Cxe5 11.Txe5 c6** entrega un peón limpio. A cambio las
negras consiguen: la columna e semiabierta contra la torre blanca, los dos alfiles
apuntando al enroque y una dama que llega a h4 y h3 con tempo. La posición tras **14...Dh3**
es la imagen de la variante: la dama negra clavada en la garganta blanca, sin nada
inmediato pero sin nada que la eche.

Muchas blancas evitan todo esto con los **anti-Marshall** (8.a4, 8.h3 o 8.d4), y eso
también dice algo sobre lo bueno que es el gambito.
""".strip(),
            theory=[
                TheorySpec(
                    title="La dama en h3 no amenaza mate",
                    kind="idea",
                    body=(
                        "Es el punto que más cuesta aceptar: **14...Dh3** no prepara ningún "
                        "mate forzado. Lo que hace es congelar al rey blanco, impedir Af1 y "
                        "obligar a las blancas a jugar el resto de la partida con una pieza "
                        "menos en el flanco de dama. El gambito se cobra en incomodidad, no "
                        "en jaques."
                    ),
                    highlight=["h3", "g3", "f1"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="espanola-berlinesa",
            name="Defensa Berlinesa",
            eco="C65-C67",
            line=RUY
            + ["Nf6", "O-O", "Nxe4", "d4", "Nd6", "Bxc6", "dxc6", "dxe5", "Nf5", "Qxd8+", "Kxd8"],
            tagline="El muro: cambiar damas en la jugada 9 y aguantar el final.",
            difficulty=4,
            drill_plies=[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            drill_difficulty=3,
            idea=(
                "Las negras entregan el derecho a enrocar a cambio de un final sin damas "
                "donde su estructura, aunque doblada, es muy difícil de atacar."
            ),
            description="""
**3...Cf6** ignora la pregunta del alfil y hace la suya: ataca e4. La línea principal
lleva a un final por la fuerza en nueve jugadas: **4.O-O Cxe4 5.d4 Cd6 6.Axc6 dxc6
7.dxe5 Cf5 8.Dxd8+ Rxd8**.

Mira la posición final con ojos del siglo XIX y es horrible para las negras: rey en d8,
peones doblados en c, no pueden enrocar. Míralas con ojos modernos y son perfectamente
jugables: **no hay damas**, así que el rey en d8 no corre peligro y camina hacia el centro
como en cualquier final; los peones doblados controlan casillas útiles; y las negras
tienen la pareja de alfiles.

Kramnik la usó para quitarle el título a Kasparov en el año 2000. Desde entonces se llama
el Muro de Berlín, y sigue en pie.
""".strip(),
            theory=[
                TheorySpec(
                    title="Un final no es una posición mala",
                    kind="structure",
                    body=(
                        "La evaluación de esta posición cambió cuando se entendió que las "
                        "debilidades sólo son debilidades si el rival puede atacarlas. Sin "
                        "damas, los peones doblados de c6 y c7 son casi imposibles de "
                        "asediar, y el rey negro llega a c7 o e7 en dos jugadas. La ventaja "
                        "blanca es real (mayoría de peones en el flanco de rey) pero pequeña."
                    ),
                    line=RUY
                    + ["Nf6", "O-O", "Nxe4", "d4", "Nd6", "Bxc6", "dxc6", "dxe5", "Nf5", "Qxd8+", "Kxd8"],
                    highlight=["c6", "c7", "d8"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="espanola-cambio",
            name="Variante del Cambio",
            eco="C68-C69",
            line=RUY
            + [
                "a6", "Bxc6", "dxc6", "O-O", "f6", "d4", "exd4", "Nxd4", "c5", "Nb3",
                "Qxd1", "Rxd1", "Bd7",
            ],
            tagline="4.Axc6: cambiar a un final con mayoría sana en el flanco de rey.",
            difficulty=2,
            drill_plies=[5, 7, 9, 11, 13, 15, 17],
            drill_difficulty=2,
            idea=(
                "Las blancas dan la pareja de alfiles para dejar a las negras con cuatro "
                "peones contra tres en el flanco de rey y peones doblados en el otro lado."
            ),
            description="""
Fischer rehabilitó esta línea en 1966 y la explicación que dio es la mejor que hay:
en el **final**, las blancas tienen una mayoría de peones sana en el flanco de rey y las
negras no pueden crear un peón pasado con su mayoría del flanco de dama, porque está
doblada.

La secuencia **5.O-O f6 6.d4 exd4 7.Cxd4 c5 8.Cb3 Dxd1 9.Txd1 Ad7** llega justo a eso.
Es una variante de conocimiento de finales disfrazada de apertura: quien sepa jugar la
estructura gana partidas sin haber calculado nada espectacular.
""".strip(),
            theory=[
                TheorySpec(
                    title="Cuenta los peones por bandos, no en total",
                    kind="structure",
                    body=(
                        "Material igual, pero mira los flancos por separado. En el de rey las "
                        "blancas tienen 4 contra 3 y pueden fabricar un peón pasado. En el de "
                        "dama las negras tienen 4 contra 3 pero con peones doblados en c, y "
                        "esa mayoría no produce nada. Ésa es toda la idea de la variante."
                    ),
                    highlight=["c6", "c7", "f2", "g2", "h2"],
                ),
            ],
            exercises=[
                ExerciseSpec(
                    ref="espanola-cambio-cambio-de-damas",
                    prompt=(
                        "Las blancas han jugado 8.Cb3. Las negras quieren el final: fuerza "
                        "el cambio de damas."
                    ),
                    setup=RUY
                    + ["a6", "Bxc6", "dxc6", "O-O", "f6", "d4", "exd4", "Nxd4", "c5", "Nb3"],
                    answer=["Qxd1", "Rxd1", "Bd7"],
                    kind="plan",
                    difficulty=2,
                    themes=["final", "cambio de damas"],
                    hint="La columna d acaba de quedarse libre.",
                    explanation=(
                        "Con **8...Dxd1 9.Txd1 Ad7** las negras entran en el final que la "
                        "variante busca desde la jugada 4. Aquí la pareja de alfiles compensa "
                        "los peones doblados, y las blancas tienen que demostrar su mayoría "
                        "del flanco de rey con técnica pura."
                    ),
                ),
            ],
        ),
        VariationSpec(
            slug="espanola-steinitz-diferida",
            name="Defensa Steinitz Diferida",
            eco="C71-C76",
            line=RUY + ["a6", "Ba4", "d6", "c3", "Bd7", "d4", "Nf6"],
            tagline="...d6 sólido, con ...a6 ya incluido para no comerse la clavada.",
            difficulty=2,
            drill_plies=[6, 7, 8, 9, 10, 11],
            drill_difficulty=2,
            idea=(
                "Defender e5 con el peón de d6 en lugar de con piezas. Posición estrecha "
                "pero sin grietas, y con el recurso ...b5 siempre disponible."
            ),
            description="""
La Steinitz original (3...d6) permite el desagradable 4.d4, porque las negras no pueden
sostener e5. Insertando **3...a6 4.Aa4** antes, el recurso ...b5 gana un tiempo crítico
y la línea se vuelve jugable.

Es la defensa de quien quiere una posición que entienda: piezas detrás de peones, poco
espacio, ninguna debilidad y un plan claro de ...Ae7, ...O-O y ...Te8 antes de pensar en
romper con ...d5 o ...c5.
""".strip(),
        ),
        VariationSpec(
            slug="espanola-schliemann",
            name="Defensa Schliemann",
            eco="C63",
            line=RUY + ["f5", "Nc3", "fxe4", "Nxe4", "d5", "Nxe5", "dxe4", "Nxc6", "Qg5"],
            tagline="3...f5: el gambito que no espera a que empiece la partida.",
            difficulty=4,
            drill_plies=[5, 6, 7, 8, 9, 10, 11, 12, 13],
            drill_difficulty=4,
            idea=(
                "Contragolpe inmediato en el centro a costa de abrir la diagonal hacia el "
                "propio rey. Con teoría es jugable; sin teoría es suicida."
            ),
            description="""
También llamada Jaenisch. **3...f5** ataca e4 antes de desarrollar una sola pieza, y
acepta a cambio que la diagonal a2-g8 y la casilla e8-h5 queden expuestas para siempre.

La línea principal **4.Cc3 fxe4 5.Cxe4 d5 6.Cxe5 dxe4 7.Cxc6 Dg5** es un ejemplo perfecto
de por qué esta apertura no se improvisa: las negras entregan una pieza durante dos jugadas
y la recuperan con un doble ataque sobre g2 y el caballo de c6. Una jugada distinta en
cualquier punto y la posición se cae.
""".strip(),
            theory=[
                TheorySpec(
                    title="El doble ataque que sostiene la variante",
                    kind="idea",
                    body=(
                        "**7...Dg5** ataca el caballo de c6 y el peón de g2 a la vez. Es la "
                        "única jugada que justifica todo el planteamiento: sin ella las negras "
                        "están simplemente una pieza abajo. Merece la pena memorizar la "
                        "posición entera."
                    ),
                    line=RUY + ["f5", "Nc3", "fxe4", "Nxe4", "d5", "Nxe5", "dxe4", "Nxc6", "Qg5"],
                    highlight=["g5", "c6", "g2"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="espanola-clasica",
            name="Defensa Clásica",
            eco="C64",
            line=RUY + ["Bc5", "c3", "Nf6", "d4", "Bb6"],
            tagline="3...Ac5: desarrollo rápido y el alfil en su mejor diagonal.",
            difficulty=2,
            drill_plies=[5, 6, 7, 8, 9],
            drill_difficulty=2,
            idea=(
                "Las negras desarrollan con la máxima naturalidad y aceptan que las blancas "
                "ganen el centro con c3 y d4, contando con reubicar el alfil en b6."
            ),
            description="""
También llamada Variante Cordel. Es la respuesta que cualquier jugador encontraría solo:
el alfil sale a su mejor casilla y ataca f2.

Las blancas responden con **4.c3**, preparando d4 y ganando un tiempo sobre el alfil.
Tras **4...Cf6 5.d4 Ab6** las negras han perdido un tiempo con el alfil, pero éste sigue
en una diagonal excelente y la posición es completamente jugable. Es una buena elección
para quien quiere jugar la Española por negras sin memorizar la Cerrada.
""".strip(),
        ),
        VariationSpec(
            slug="espanola-arkhangelsk",
            name="Variante Arcángel",
            eco="C78",
            line=RUY + ["a6", "Ba4", "Nf6", "O-O", "b5", "Bb3", "Bb7"],
            tagline="...b5 y ...Ab7: los dos alfiles apuntando al enroque blanco.",
            difficulty=3,
            drill_plies=[7, 8, 9, 10, 11],
            drill_difficulty=3,
            idea=(
                "Las negras renuncian a ...Ae7 para poner el alfil en la diagonal larga, "
                "presionando e4 y g2 desde el primer momento."
            ),
            description="""
Llamada así por la ciudad rusa donde se analizó. La idea es agresiva: en vez del modesto
...Ae7, las negras juegan **...Ab7** y a menudo **...Ac5**, con los dos alfiles apuntando
al rey blanco.

El coste es que el rey negro tarda más en enrocar y el centro queda menos apuntalado. La
Arcángel es para quien quiere posiciones dinámicas con negras y está dispuesto a calcular.
""".strip(),
        ),
        VariationSpec(
            slug="espanola-worrall",
            name="Ataque Worrall",
            eco="C86",
            line=RUY + ["a6", "Ba4", "Nf6", "O-O", "Be7", "Qe2", "b5", "Bb3", "d6", "c3", "O-O", "Rd1"],
            tagline="6.De2 en lugar de 6.Te1: la dama defiende e4 y la torre va a d1.",
            difficulty=3,
            drill_plies=[10, 11, 12, 13, 14, 16],
            drill_difficulty=3,
            idea=(
                "Al defender e4 con la dama, la torre de f1 queda libre para d1, donde apoya "
                "el avance d4 en lugar de vigilar la columna e."
            ),
            description="""
Un cambio de orden pequeño con consecuencias grandes. **6.De2** defiende e4 igual que
6.Te1, pero libera la torre para **Td1**, donde apoya directamente la ruptura d4.

Como efecto colateral, la Worrall esquiva por completo el Ataque Marshall: sin torre en
e1, el sacrificio ...d5 pierde buena parte de su sentido. Muchos jugadores la eligen
exactamente por eso.
""".strip(),
        ),
        VariationSpec(
            slug="espanola-celadas",
            name="Celadas de la Española",
            eco="C60-C70",
            line=RUY + ["Nd4"],
            tagline="Las trampas que hay que conocer para no caer en ellas.",
            difficulty=3,
            drill_plies=[],
            idea=(
                "Posiciones concretas donde una jugada natural pierde por la fuerza. "
                "Se estudian una vez y se recuerdan siempre."
            ),
            description="""
La Española es lenta, pero tiene puntos afilados. Estas celadas aparecen en partidas de
club constantemente, y las dos castigan jugadas que parecen perfectamente razonables:
coger un peón en el centro y coger un peón en e5.
""".strip(),
            exercises=[
                ExerciseSpec(
                    ref="espanola-celada-arca-de-noe",
                    prompt=(
                        "Trampa del Arca de Noé. Las blancas acaban de coger el peón con "
                        "8.Dxd4. Atrapa el alfil de b3 en cuatro jugadas."
                    ),
                    setup=RUY + ["a6", "Ba4", "d6", "d4", "b5", "Bb3", "Nxd4", "Nxd4", "exd4", "Qxd4"],
                    answer=["c5", "Qd5", "Be6", "Qc6+", "Bd7", "Qd5", "c4"],
                    kind="trap",
                    difficulty=4,
                    themes=["pieza atrapada", "celada", "peones"],
                    hint="Los peones de c y b forman una jaula. Empieza expulsando la dama.",
                    explanation=(
                        "El nombre viene de la jaula de peones a6-b5-c4 que encierra al alfil. "
                        "Tras **11...c4** el alfil de b3 sólo tiene a4, donde ...b5xa4 lo recoge: "
                        "c2 y a2 están ocupadas por peones propios y la diagonal hacia d1 está "
                        "cerrada. Es la razón por la que las blancas no juegan d4 antes de c3 "
                        "en estas estructuras."
                    ),
                ),
                ExerciseSpec(
                    ref="espanola-celada-defensa-bird",
                    prompt=(
                        "Tras 3...Cd4 las blancas han jugado 4.Cxe5. Encuentra la refutación "
                        "y remátala: son siete jugadas hasta el mate."
                    ),
                    setup=RUY + ["Nd4", "Nxe5"],
                    answer=["Qg5", "Nxf7", "Qxg2", "Rf1", "Qxe4+", "Be2", "Nf3#"],
                    kind="trap",
                    difficulty=4,
                    expect="mate",
                    themes=["mate", "clavada", "celada"],
                    hint="Empieza con un doble ataque sobre el caballo y g2.",
                    explanation=(
                        "El remate depende de una clavada: tras 7.Ae2 el alfil no puede capturar "
                        "en f3 porque está clavado por la dama de e4 contra su propio rey. Por eso "
                        "**7...Cf3** es mate y no un simple jaque."
                    ),
                ),
            ],
        ),
    ],
)

/* Spanish algebraic notation.
 *
 * The backend stores standard English SAN, which is what chess.js and Stockfish
 * speak. Spanish players read R-D-T-A-C, so the translation happens here, at the
 * last possible moment before the text is shown.
 */

const PIECES = { K: 'R', Q: 'D', R: 'T', B: 'A', N: 'C' }

/** "Nf3" -> "Cf3", "Qxd1" -> "Dxd1", "O-O" -> "O-O". */
export function toSpanish(san) {
  if (!san) return ''
  if (san.startsWith('O-O')) return san
  const initial = san[0]
  return PIECES[initial] ? PIECES[initial] + san.slice(1) : san
}

/**
 * Group a flat SAN list into score-sheet rows.
 * `startPly` is 0 when the list begins with a White move.
 */
export function toMovePairs(sanMoves, startPly = 0) {
  const rows = []
  sanMoves.forEach((san, index) => {
    const ply = startPly + index
    const number = Math.floor(ply / 2) + 1
    const isWhite = ply % 2 === 0
    if (isWhite) {
      rows.push({ number, white: toSpanish(san), black: '', whiteIndex: index, blackIndex: null })
    } else if (rows.length) {
      rows[rows.length - 1].black = toSpanish(san)
      rows[rows.length - 1].blackIndex = index
    } else {
      rows.push({ number, white: '', black: toSpanish(san), whiteIndex: null, blackIndex: index })
    }
  })
  return rows
}

/** "1.e4 e5 2.Cf3" for inline use in prompts and lists. */
export function toInlineLine(sanMoves, startPly = 0, limit = Infinity) {
  const parts = []
  sanMoves.slice(0, limit).forEach((san, index) => {
    const ply = startPly + index
    const number = Math.floor(ply / 2) + 1
    if (ply % 2 === 0) parts.push(`${number}.${toSpanish(san)}`)
    else if (index === 0) parts.push(`${number}...${toSpanish(san)}`)
    else parts.push(toSpanish(san))
  })
  const line = parts.join(' ')
  return sanMoves.length > limit ? `${line}…` : line
}

/** Centipawns as players read them: +1.24, -0.35, M4. */
export function formatScore(scoreCp, mateIn) {
  if (mateIn !== null && mateIn !== undefined) {
    return `M${Math.abs(mateIn)}`
  }
  if (scoreCp === null || scoreCp === undefined) return '—'
  const pawns = scoreCp / 100
  return `${pawns > 0 ? '+' : ''}${pawns.toFixed(2)}`
}

export const KIND_LABELS = {
  theory: 'Teoría',
  tactic: 'Táctica',
  plan: 'Plan',
  trap: 'Celada',
  recall: 'Memoria',
}

export const DIFFICULTY_LABELS = {
  1: 'Introductorio',
  2: 'Fácil',
  3: 'Medio',
  4: 'Difícil',
  5: 'Experto',
}

export const STATUS_LABELS = {
  unseen: 'Sin hacer',
  solved: 'Resuelto',
  failed: 'Fallido',
}

/** "1 min 12 s" — durations are always short here, so no hours. */
export function formatDuration(ms) {
  if (!ms) return '—'
  const seconds = Math.round(ms / 1000)
  if (seconds < 60) return `${seconds} s`
  return `${Math.floor(seconds / 60)} min ${String(seconds % 60).padStart(2, '0')} s`
}

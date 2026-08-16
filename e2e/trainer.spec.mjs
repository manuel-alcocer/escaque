/**
 * End-to-end regression test for the exercise runner.
 *
 * Guards one specific bug: moving to the next exercise left the board unable to
 * accept moves. Chessground binds its pointer listeners inside redrawAll() and
 * skips them when the board is viewOnly; its set() runs redrawAll() for an
 * orientation change *before* applying the rest of the config, so a board that
 * had just finished an exercise (viewOnly) and then received the next one
 * (interactive, other side) was redrawn while still marked viewOnly and ended
 * up with no listeners. Refreshing the page hid it, which is why it looked like
 * a data problem.
 *
 * The test needs no knowledge of the solutions: it walks several exercises with
 * "Ver solución" and, on each one, asserts the board is alive by tapping pieces
 * until one offers legal destinations. A live board always has at least one.
 *
 *   node trainer.spec.mjs                     # against http://localhost:8080
 *   BASE=http://... USER=x PASS=y node trainer.spec.mjs
 */

import { chromium } from 'playwright'

const BASE = process.env.BASE || 'http://localhost:8080'
const USER = process.env.USER_NAME || 'manuel'
const PASS = process.env.USER_PASS || 'ajedrez2026!'
const EXERCISES = Number(process.env.EXERCISES || 5)
const CHROME = process.env.CHROME_PATH || undefined

const browser = await chromium.launch({ executablePath: CHROME })
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
})
const page = await context.newPage()

const problems = []
page.on('pageerror', (error) => problems.push(`error de página: ${error.message}`))

async function signIn() {
  await page.goto(`${BASE}/entrar`)
  await page.fill('input[name=username]', USER)
  await page.fill('input[name=password]', PASS)
  await page.click('button[type=submit]')
  await page.waitForURL(`${BASE}/`)
}

/** Centres of the pieces currently on the board, in viewport coordinates. */
function pieceCentres() {
  return page.evaluate(() => {
    const board = document.querySelector('cg-board')
    if (!board) return []
    const rect = board.getBoundingClientRect()
    const square = rect.width / 8
    return [...board.querySelectorAll('piece')].map((piece) => {
      const match = /translate\(([-\d.]+)px,\s*([-\d.]+)px\)/.exec(piece.style.transform || '')
      const x = match ? Number(match[1]) : 0
      const y = match ? Number(match[2]) : 0
      return { x: rect.x + x + square / 2, y: rect.y + y + square / 2 }
    })
  })
}

const destinationCount = () =>
  page.evaluate(() => document.querySelectorAll('cg-board square.move-dest').length)

/**
 * A board is alive if tapping some piece reveals its legal destinations.
 * Tapping a piece of the side that is not to move is a no-op, so we try
 * several before concluding the board is dead.
 */
async function boardAcceptsInput() {
  for (const centre of await pieceCentres()) {
    await page.touchscreen.tap(centre.x, centre.y)
    await page.waitForTimeout(120)
    if ((await destinationCount()) > 0) {
      await page.touchscreen.tap(centre.x, centre.y) // deselect
      return true
    }
  }
  return false
}

await signIn()
await page.goto(`${BASE}/entrenar?variation=caro-kann-avance`)
await page.waitForTimeout(1500)

for (let index = 1; index <= EXERCISES; index += 1) {
  const prompt = (await page.locator('.trainer__task').textContent().catch(() => '')) || ''
  const wrap = await page.evaluate(() => document.querySelector('.cg-wrap')?.className || '')
  const alive = await boardAcceptsInput()

  console.log(
    `[${index}] ${alive ? 'vivo ' : 'MUERTO'} · ${wrap.includes('orientation-black') ? 'negras' : 'blancas'} · ${prompt.slice(0, 42)}`,
  )
  if (!alive) problems.push(`ejercicio ${index}: el tablero no acepta movimientos`)

  if (index === EXERCISES) break

  // End this exercise without needing to know its answer, then advance.
  const giveUp = page.locator('.actions .btn', { hasText: 'Ver solución' })
  if (await giveUp.count()) await giveUp.click()
  await page.waitForTimeout(900)
  const next = page.locator('.actions .btn--primary')
  if (!(await next.count())) {
    problems.push(`ejercicio ${index}: no apareció el botón para continuar`)
    break
  }
  await next.click()
  await page.waitForTimeout(1500)
}

await browser.close()

if (problems.length) {
  console.error(`\nFALLOS (${problems.length}):`)
  problems.forEach((problem) => console.error(`  - ${problem}`))
  process.exit(1)
}
console.log(`\nOK: los ${EXERCISES} tableros aceptaron movimientos.`)

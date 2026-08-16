import DOMPurify from 'dompurify'
import { marked } from 'marked'

/** Render a one-paragraph snippet (an explanation, a caption) as inline HTML. */
export function renderInline(source) {
  return DOMPurify.sanitize(marked.parseInline(source || ''))
}

/** Render a full Markdown document. */
export function renderBlock(source) {
  return DOMPurify.sanitize(marked.parse(source || ''))
}

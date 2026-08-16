<script setup>
/**
 * Theory prose. The content comes from our own seed, but it is editable from the
 * Django admin, so it is sanitised before it reaches the DOM.
 */
import DOMPurify from 'dompurify'
import { marked } from 'marked'
import { computed } from 'vue'

const props = defineProps({
  source: { type: String, default: '' },
})

marked.setOptions({ gfm: true, breaks: false })

const html = computed(() => DOMPurify.sanitize(marked.parse(props.source || '')))
</script>

<template>
  <div class="prose" v-html="html"></div>
</template>

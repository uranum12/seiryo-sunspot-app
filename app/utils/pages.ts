import type { Component } from "svelte"

type PageWithChild = {
  path: string
  name: string
  page?: Component
  children: Page[]
}

type PageOnly = {
  path: string
  name: string
  page: Component
}

export type Page = PageWithChild | PageOnly

export type Path = {
  path: string
  name: string
  selected: boolean
}

function isPageWithChild(page: Page): page is PageWithChild {
  return "children" in page
}

export function searchPage(
  path: string[],
  pages: Page[],
): Component | undefined {
  if (path.length <= 0) {
    return undefined
  }
  for (const page of pages) {
    if (page.path === path[0]) {
      if (path.length === 1) {
        return page.page
      }
      if (isPageWithChild(page)) {
        return searchPage(path.slice(1), page.children)
      }
    }
  }
  return undefined
}

function buildPath(page: Page): string {
  if (!isPageWithChild(page)) {
    return page.path
  }
  if (page.page) {
    return page.path
  }
  return `${page.path}/${buildPath(page.children[0])}`
}

function formatPath(
  parentPath: string,
  currentPath: string,
  pages: Page[],
): Path[] {
  return pages.map((page) => ({
    path: `${parentPath}/${buildPath(page)}`,
    name: page.name,
    selected: currentPath === page.path,
  }))
}

export function searchPath(
  path: string[],
  pages: Page[],
  parentPath = "#",
): Path[][] {
  const paths = formatPath(parentPath, path.length ? path[0] : "", pages)
  for (const page of pages) {
    if (path.length > 0 && page.path === path[0]) {
      if (isPageWithChild(page)) {
        return [paths].concat(
          searchPath(path.slice(1), page.children, `${parentPath}/${path[0]}`),
        )
      }
    }
  }
  return [paths]
}

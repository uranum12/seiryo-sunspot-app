import { mount } from "svelte"

import App from "./app.svelte"

import "purecss/build/base.css"
import "purecss/build/forms.css"
import "purecss/build/buttons.css"
import "purecss/build/menus.css"
import "purecss/build/grids.css"
import "purecss/build/tables.css"

mount(App, {
  target: document.body,
})

import { homedir } from "node:os"

type Route = { name: string; params?: { sessionID?: string } }
type Session = { directory?: string }
type Api = {
  route?: { current?: Route }
  state?: {
    path?: { directory?: string }
    session?: { get(id: string): Session | undefined }
  }
  renderer?: { isDestroyed?: boolean; setTerminalTitle?: (title: string) => void }
}

function shorten(dir: string): string {
  const home = homedir()
  let p = dir
  if (p === home) return "~"
  if (p.startsWith(home + "/")) p = "~" + p.slice(home.length)
  p = p.replace("~/anaconda/", "🅐 /")
  p = p.replace("~/pypy/misc/", "🅟 /🅜 /")
  p = p.replace("~/pypy/misc", "🅟 /🅜 /")
  p = p.replace("~/pypy/", "🅟 /")
  return p
}

async function tui(api: Api) {
  let last: string | undefined

  const update = () => {
    try {
      const route = api?.route?.current
      let dir = api?.state?.path?.directory
      if (!dir) return
      if (route?.name === "session") {
        const id = route.params?.sessionID
        const session = id ? api.state?.session?.get(id) : undefined
        if (session?.directory) dir = session.directory
      }
      const title = `🟨 ${shorten(dir)}`
      if (title === last) return
      const renderer = api?.renderer
      if (!renderer || renderer.isDestroyed) return
      if (typeof renderer.setTerminalTitle !== "function") return
      renderer.setTerminalTitle(title)
      last = title
    } catch {
    }
  }

  update()
  const timer = setInterval(() => {
    try {
      if (api?.renderer?.isDestroyed) {
        clearInterval(timer)
        return
      }
      update()
    } catch {
    }
  }, 500)
}

export default { id: "kilo-antocuni", tui }

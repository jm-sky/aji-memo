'use client'

import { MailIcon, MapPinIcon } from "lucide-react"
import LinkUnderline from "../ui/link-underline"
import { LogoText } from "../ui/logo-text"

export default function AddressFooter() {
  return (
    <section className="py-20 bg-black text-white">
      <div className="container mx-auto px-4 md:px-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="flex flex-col gap-4">
          <LogoText size="xl" className="text-3xl sm:text-4xl mb-4 tracking-tight" />
        </div>
        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-4">
            <MapPinIcon className="size-4" />
            <LinkUnderline href="https://maps.app.goo.gl/1234567890"  >
              Warszawa, Poland
            </LinkUnderline>
          </div>
          <div className="flex items-center gap-4">
            <MailIcon className="size-4" />
            <LinkUnderline href="mailto:contact@ajimemo.com">
              contact@ajimemo.com
            </LinkUnderline>
          </div>
        </div>
      </div>
    </section>
  )
}

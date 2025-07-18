'use client'

import { motion, useInView } from 'framer-motion'
import SparklesLogo from '@/components/mvpblocks/sparkles-logo'
import {
  Building2,
  Search,
  Zap,
  ArrowRight,
  CheckCircle
} from 'lucide-react'
import { CardHoverEffect } from '../ui/pulse-card'
import { useRef } from 'react'
import { ButtonLink } from '../ui/button-link'
import AddressFooter from './address-footer'
import LandingNav from './landing-nav'

export default function LandingPage() {
  const featuresRef = useRef(null);

  const featuresInView = useInView(featuresRef, { once: true, amount: 0.3 });

  const features = [
    {
      icon: Building2,
      title: 'Save memories',
      description: 'Save memories of your conversations with Ai'
    },
    {
      icon: Search,
      title: 'Smart Search',
      description: 'Find memories instantly with our advanced search and filtering capabilities.'
    },
    {
      icon: Zap,
      title: 'Share memories',
      description: 'Share memories with your friends and family or team'
    }
  ]

  const benefits = [
    'Universal access by GET request',
    'REST API with comprehensive documentation',
  ]

  return (
    <div className="min-h-screen bg-background overflow-hidden">
      {/* Navigation */}
      <LandingNav />

      <motion.div
        initial={{ opacity: 0, scale: 1.2 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="flex items-center justify-center"
      >
        <div className="relative w-full">
          <SparklesLogo />
        </div>
      </motion.div>

      {/* Hero Section with Sparkles */}
      <section className="relative overflow-hidden py-20 lg:py-32">
        <div className="container relative z-10 mx-auto px-4 md:px-6">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="flex flex-col justify-center space-y-8"
          >
            <div className="space-y-4">
              <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl md:text-6xl">
                Ai Memory
                <span className="bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
                  {' '}API
                </span>
              </h1>
              <p className="text-xl text-muted-foreground max-w-[600px]">
                Extended memory for Ai
                Perfect for Ai to remember your conversations and preferences.
              </p>
            </div>

            <div className="flex flex-col gap-4 sm:flex-row">
              <ButtonLink
                size="lg"
                href="/register"
                className="group"
                variant="brand"
                vibe="primary"
              >
                Start Free Trial
                <ArrowRight className="ml-2 size-4 group-hover:translate-x-1 transition-transform" />
              </ButtonLink>
              <ButtonLink
                size="lg"
                variant="outline"
                href="/docs"
              >
                View Documentation
              </ButtonLink>
            </div>

            <div className="flex flex-col gap-2">
              <p className="text-sm text-muted-foreground">Trusted by developers:</p>
              <div className="flex items-center gap-4">
                {benefits.slice(0, 3).map((benefit, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <CheckCircle className="size-4 text-green-500" />
                    <span className="text-sm text-muted-foreground">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-muted/50 relative">
        {/* Colorful Light Effects */}
        <div className="absolute inset-0 overflow-hidden opacity-80">
          <div className="absolute top-0 left-0 size-96 bg-gradient-to-r from-brand/30 to-brand/10 rounded-full blur-3xl" />
          <div className="absolute top-1/3 right-1/8 size-80 bg-gradient-to-r from-brand/25 to-brand/15 rounded-full blur-3xl" style={{ animationDelay: '1s' }} />
          <div className="absolute bottom-1/3 right-1/2 size-56 bg-gradient-to-r from-brand/25 to-brand/15 rounded-full blur-3xl" style={{ animationDelay: '1.5s' }} />
        </div>

        <div className="container mx-auto px-4 md:px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Everything you need for Polish business data
            </h2>
            <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
              Comprehensive API platform providing access to official Polish business registries
            </p>
          </motion.div>

          <div ref={featuresRef} className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                animate={
                  featuresInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }
                }
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="group relative flex"
              >
                <CardHoverEffect
                  icon={<feature.icon className="size-6" />}
                  title={feature.title}
                  description={feature.description}
                  glowEffect={true}
                  variant="blue"
                  size="lg"
                />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 md:px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl mb-4">
              Ready to get started?
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              Join thousands of developers using AjiMemo to access Polish business data
            </p>
            <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
              <ButtonLink
                size="lg"
                href="/register"
                variant="brand"
                vibe="primary"
                className="group"
              >
                Start Free Trial
                <ArrowRight className="ml-2 size-4 group-hover:translate-x-1 transition-transform" />
              </ButtonLink>
              <ButtonLink
                size="lg"
                variant="outline"
                href="/login"
              >
                Sign In
              </ButtonLink>
            </div>
          </motion.div>
        </div>
      </section>

      <AddressFooter />
    </div>
  )
}

---
title: Contato
date: 2021-12-18T03:10:36.000Z
draft: false
language: pt
description: Página de contato com formulário
---

<!-- @format -->

<section class="lg:pb-24">
  <div class="max-w-screen-md px-4 mx-auto">
      <p class="mb-8 font-light text-center text-gray-500 lg:mb-16 dark:text-gray-400 sm:text-xl">Tem algum problema técnico? Quer enviar comentários sobre um recurso em teste? Precisa de detalhes sobre nossos planos? Entre em contato conosco.</p>
      <form name="contact" netlify class="space-y-8">
          <div class="my-4">
              <label for="email" class="block mb-2 font-medium text-gray-900 text-md dark:text-gray-300"><strong>Seu Email:</strong></label>
              <input type="email" id="email" class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-md rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-500 dark:focus:border-indigo-500 dark:shadow-sm-light" placeholder="seu.email@exemplo.com" required>
          </div>
          <div class="my-4">
              <label for="subject" class="block mb-2 font-medium text-gray-900 text-md dark:text-gray-300"><strong>Assunto:</strong></label>
              <input type="text" id="subject" class="block w-full p-3 text-gray-900 border border-gray-300 rounded-lg shadow-sm text-md bg-gray-50 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-500 dark:focus:border-indigo-500 dark:shadow-sm-light" placeholder="Nos conte como podemos ajudá-lo" required>
          </div>
          <div class="my-4 sm:col-span-2">
              <label for="message" class="block mb-2 font-medium text-gray-900 text-md dark:text-gray-400"><strong>Sua mensagem:</strong></label>
              <textarea id="message" rows="6" class="block p-2.5 w-full text-md text-gray-900 bg-gray-50 rounded-lg shadow-sm border border-gray-300 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-500 dark:focus:border-indigo-500" placeholder="Deixe seu comentário..."></textarea>
          </div>
          <div class="mt-6 lg:pb-16">
             <button type="submit" class="px-5 py-3 font-bold text-center text-white bg-indigo-600 rounded-lg text-md sm:w-fit hover:bg-indigo-800 focus:ring-4 focus:outline-none focus:ring-indigo-300 dark:bg-indigo-600 dark:hover:bg-indigo-700 dark:focus:ring-indigo-800">Enviar Mensagem</button>
          </div>
      </form>
  </div>
</section>

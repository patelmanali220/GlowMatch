package com.glowmatch;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class GlowmatchBackendApplication {

	public static void main(String[] args) {
		SpringApplication.run(GlowmatchBackendApplication.class, args);
		System.out.println("\n============================================================");
		System.out.println("🌟 GlowMatch Backend Started Successfully!");
		System.out.println("============================================================");
		System.out.println("🔗 Server running at: http://localhost:8080");
		System.out.println("📡 API Base URL: http://localhost:8080/api/v1");
		System.out.println("🤖 ML Service: http://localhost:8001");
		System.out.println("============================================================\n");
	}

	@Bean
	public RestTemplate restTemplate(@Value("${ml.service.timeout:30000}") int timeoutMs) {
		SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
		factory.setConnectTimeout(timeoutMs);
		factory.setReadTimeout(timeoutMs);
		return new RestTemplate(factory);
	}

}
